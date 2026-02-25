#!/usr/bin/perl

use warnings;
use strict;

package Server;

use HTTP::Server::Simple::CGI;
use File::Slurp;

use base "HTTP::Server::Simple::CGI";
our %TYPES = (
	html => "text/html",
	jpg => "image/jpeg",
	gif => "image/gif",
	png => "image/png",
	swf => "application/x-shockwave-flash",
);

sub handle_request {
	my ($self, $cgi) = @_;

	my $path = $cgi->path_info;
	if (-d "./$path") {
		$path = "$path/index.html";
	}
	if (-x "./$path") {
		print "HTTP/1.0 200 OK\r\n";
		print `./$path`;
	}
	elsif (-e "./$path") {
		print "HTTP/1.0 200 OK\r\n";
		my @pieces = split /\./, $path;
		print "Content-Type: $TYPES{$pieces[-1]}\r\n" if ($TYPES{$pieces[-1]});
		print "\r\n";
		print File::Slurp::read_file("./$path");
	}
	else {
		print "HTTP/1.0 404 Not Found\r\n\r\n";
	}
}

package main;

my $server = Server->new;
print "Server's PID is ", $server->background, "\n";
