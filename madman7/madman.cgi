#!/usr/bin/perl
use CGI qw/:standard/;
print header;

$prefix = './';
#$prefix = "/home/james/l/leonardr/public_html/madman7/";
$notes_file = $prefix."notes.mml";
$text_file = $prefix."text.mml";
$image_url = "triangle.gif";

%info = ();
%discourse = ();
%style = ();
%plot = ();

%titles = ("info" => "Footnote",
	   "style" => "Figure of STYLE (Trope)",
	   "plot" => "Figure of PLOT (Topos)",
	   "discourse" => "Figure of DISCOURSE (Dialog)",
	   );

@valid_actions = ("show_text","expand_node",
		  "expand_subnode","expand_glossary");
@subnodes = ("info","style","plot","discourse");

@nodes_with_long_message = ("diary","madman","dressed_quickly","number","everybody_says_so");

#Get the notes.
@note_list = ();
open NOTES, $notes_file;
while (get_next_note()) {};
#print_note_stats();
#exit;

#Get user parameters.
$action = param("action") or $action = "show_text";
if ($action ne "show_text") { $node = param("node"); }
if ($action eq "expand_node") { $enabled_subnode = param("enabled_subnode"); }
if ($action eq "expand_subnode") { $subnode = param("subnode"); }
if ($action eq "expand_glossary") { $glossary_item = param("glossary_item"); }

#We now know exactly what they want to do. So we output some text.
if ($action eq "show_text")
{
    print_text();
} elsif ($action eq "expand_node") {
    expand_node($node,$enabled_subnode);
} elsif ($action eq "expand_subnode") {
    expand_subnode($node,$subnode);
} elsif ($action eq "expand_glossary") {
    expand_glossary($node,$glossary_item);
}

sub next_avaliable_subnode
{
    ($node,$current_subnode) = @_;
    my $start_checking = 0;
    if ($current_subnode eq "")
    {
	$start_checking = 1;
    }

    #Find the current_subnode
    @order_list = split " ", $order{$node};
    foreach $subnode (@order_list)
    {
	if ((!$start_checking) && $subnode eq "$current_subnode")
	{
	    $start_checking = 1;
	} elsif ($start_checking) {
	    if ($notes{$node}{$subnode})
	    {
		return $subnode;
	    } else {
	    }
	}
    }
}

sub expand_subnode
{
    my ($node, $subnode) = @_;
    print_body_standard("F5F5B0");
    print title($titles{$subnode},1);
    print "<p><b>$keyword{$node}</b></p>";

    print link_glossaries($node,"<p>$notes{$node}{$subnode}</p>");
    my $link_text;

    if (next_avaliable_subnode($node,$subnode))
    {	
	$node_url = "madman.cgi?action=expand_node&node=$node&enabled_subnode=$subnode";
	$link_text = "Return to top frame";
    } else {
	$node_url = "cell.white.html";	
	$link_text = "Finished with the construal. Return to the main text.";
	foreach $n (@nodes_with_long_message)
	{
	    if ($n eq $node)
	    {
		$link_text = "Finished with the construal of \"$keyword{$node}\" Click here to return to the main text.";
	    }
	}
    }

    if (fancy())
    {
	print <<END;
<script language="javascript">
    <!--
	function loadbar() {
	 parent.bar.window.location="$node_url";	 
         self.location="cell.white.html";
         parent.glossary.window.location="cell.blue.html";
	}
     //-->
</script>
    <p><a href="javascript:loadbar()">$link_text</a></p>
END
       	
} else {
    
    print "<p><a href=\"$node_url\">Continue</a></p>";
}
}

sub expand_node
{
    my ($node) = @_;
    if (!$notes{$node})
    {
	print "<h1>Error:</h1><p>The node $node does not exist.</p>";
    }
    print_body_standard("ffffff");
    print "<font size=-1>";
    print highlight($context{$node});
    print_menu_bar($node,next_avaliable_subnode($node,$enabled_subnode));
    print "</font>";
}

sub print_menu_bar
{
    my ($node,$enabled_subnode) = @_;
    unless ($enabled_subnode)
    {
	print "<p>Return to the main Madman text.</p>";
	return;
    }
       
    print "<b>";

    print "| ";

    foreach $subnode (@subnodes)
    {
	if ($subnode eq $enabled_subnode)
	{
	    make_subnode_expand_link($node,$subnode);
	} else {
	    print ucfirst($subnode) . " | ";
	}
    }
    print "</b>";
}

########################################################################

sub fancy()
{
    $browser = $ENV{'HTTP_USER_AGENT'};
    if ($browser =~ /Lynx/)
    {
	return 0;
    } else {
	return 1;
    }
}

sub expand_glossary($node,$glossary_item)
{
    print_body_standard("8cc8f3");
    if ($glossary{$node}{$glossary_item})
    {
	print "<p><b>$glossary_item</b></p>\n";
	print "<p>$glossary{$node}{$glossary_item}</p>\n";
    } else {
	print "<p>Error: Couldn't find glossary item $glossary_item for node $node.\n";
    }

    print "<p><a href=\"cell.blue.html\">Continue reading</a></p>" if fancy();
}


sub link_glossaries
{
    my ($node, $text) = @_;
    if (fancy()) {$target = " target=\"glossary\"";} else {$target = "";}

    $r = "<a href=\"madman.cgi?action=expand_glossary&node=$node";

    while ($text =~ /<g "([^>]*)">/)
    {
	$item = $1;
	$encoded_item = hex_encode($item);	
	$text =~ s#<g "$item">#$r&glossary_item=$encoded_item" $target>$item</a>#g;
    }
    return $text;
}

sub make_subnode_expand_link
{
    my ($node, $subnode) = @_;
    print "<blink><a href=\"madman.cgi?action=expand_subnode&node=$node&subnode=$subnode\"";
    if (fancy()) { print "target = notes"; }
    print ">";
    print ucfirst($subnode);
    print "</a></blink> | ";
}

sub print_text
{
    open TEXT, $text_file;
    while (<TEXT>)
    {
#	chomp();
	$text .= $_;
    }

    if (fancy()) 
    {
	$target .= " target=\"bar\"";
	$link_text = "<img src=\"$image_url\" border= \"0\">";
    } else {
	$target = "";
	$link_text = "*";
    }

    if (fancy())
    {
	until ($text !~ /<node "(.*?)">/)
	{	    
	    $node_name = $1;
	    $link = "<a href=\"javascript:loadbar(&quot;$node_name&quot;)\">$link_text</a>";
	    $text =~ s#\n([^\n]*)\n([^\n]*)<node "$node_name">#\n<a name="$node_name">$1\n$2$link</a>#g;
	}
    } else {
        $text =~ s/<node "([^>]*)">/<a href="madman.cgi?action=expand_node&node=$1\"$target>$link_text<\/a>/g;
    }


print "<html>";
print_body_standard("ffffff");

    print <<END;
<script language="javascript">
<!--
 function loadbar(str) 
 {
  str1="madman.cgi?action=expand_node&node="+str
  parent.bar.window.location=str1;
  self.location=("madman.cgi#"+str);
 }
//-->
</script>
END
    print $text;
    print "</body>";
    print "</html>";
}

sub get_next_note
{
    $node_name = "";
    $node = "";
    if (eof(NOTES) || !($line = <NOTES>)) { return 0; }	    
    while (!eof(NOTES) && $line !~ /<note/) {$line = <NOTES>;}
    return 0 if eof(NOTES);
    if ($line !~ /^\s*<note "(.*)">\s*$/)
    {
	die "Can't deal with line $line. Need <note \"x\"> by itself.";
    }

    $node_name = $1;
    push @note_list, $node_name;

    $note = "";
    while (($line = <NOTES>) && $line !~ /<\/note>/)
    {
	$node .= $line;
    }

    $node =~ s#\n\s*# #g;
    $node =~ m#<order\s*?"([^>]*?)"\s*>#i;
    if ($1) { $order{$node_name} = $1; } else { $order{$node_name} = join " ", @subnodes;}

    $node =~ m#<keyword>(.*?)</keyword>#i;
    $keyword{$node_name} = $1;

    $node =~ m#<context>(.*?)</context>#i;
    $context{$node_name} = $1; 

    foreach $subnode (@subnodes)
    {
	if ($node =~ m#<$subnode>(.*?)</$subnode>#i)
	{
	    $notes{$node_name}{$subnode} = $1;
	}
    }

    while ($node =~ m#<gloss "([^>]*)">(.*?)</gloss>#g)
    {	
	$glossary{$node_name}{$1} = $2;
    }
    return 1;

}

sub print_note_stats
{
    print "I know about ".scalar(@note_list)." notes.\n\n";
    foreach $note_name (@note_list)
    {
	print "Note $note_name.<ul>\n";
	print " <li>Keyword: $keyword{$note_name}\n";
	print " <li>Context: $context{$note_name}\n";

	foreach $key (keys %{$notes{$note_name}})
	{
	    print "<li>$key:\n $notes{$note_name}{$key}\n\n";
	}

	foreach $key (keys %{$glossary{$note_name}})
	{	    
	    print "<li>Glossary entry $key:\n $glossary{$note_name}{$key}\n\n";
	}
	print "</ul>";
    }
}

sub highlight
{
    ($oldver) = @_;
    $oldver =~ s/<h>/<b><font color=\"green\">/;
    $oldver =~ s/<\/h>/<\/font><\/b>/;
    $newver = "$oldver<br>";
}

sub title
{
    ($t,$grandiosity) = @_;
    if ($grandiosity == 0)
    {
	return "<p><b>$t</b></p>";
    } elsif ($grandiosity == 1) {
	return "<h4>$t</h4>";
    }

}

sub hex_encode
{
    ($t) = @_;
    $t =~ s/ /%20/g;
    return $t;
}

sub print_body
{
    my ($text,$bg,$link,$vlink,$alink) = @_;

    print "<body ";
    print "text=\"\#$text\"";
    print "bgcolor=\"\#$bg\"";
    print "link=\"\#$link\""; 
    print "vlink=\"\#$vlink\"";
    print "alink=\"\#$alink\">";
    print "\n\n";
}

sub print_body_standard
{
    my ($bg) = @_;
    print_body("000000",$bg,"0000ff","551a8b","0000ff");
}
