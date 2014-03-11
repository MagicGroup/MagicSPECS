#!/usr/bin/perl
# autogenerate a man page for tla/baz from tla/baz output
# Copyright 2005 Hans Ulrich Niedermann
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# BUGS:
#  - ?


use strict;


########################################################################
# man_escape($string)
#
# Escape special characters for man page output.

sub man_escape()
{
    my ($string) = (@_);
    #$string =~ s|\\|\\\\|g;
    $string =~ s|\`|\\\`|g;
    $string =~ s|\'|\\\'|g;
    $string =~ s|-|\\-|g;
    return($string);
}


########################################################################
# build_section_list($tlacmd)
#
# Iterate over the output of "tla help" and build a data structure
# with the sections, commands and short descriptions.
#
# We will later use that data structure to
#   * create a short outline
#   * run "tla $cmd -H" for detailed help sections on each command

sub build_section_list()
{
    my ($tlacmd) = (@_);
    my @sections = ();
    my @commands = ();
    my $section = {};
    open(HELP, '-|', "$tlacmd", 'help')
	or die "Cannot run \`$tlacmd help'! $!";
    while (<HELP>) {
	chomp;
	if (/^$/) {
	    # ignore empty lines
	} elsif (/^\s*([^:]+)\s+:\s+(.+)\s*$/) {
	    my ($cmdname, $descr) = ($1,$2);
	    #print "cmd:   $cmdname\ndescr: $descr\n\n";
	    push(@commands, [$cmdname, $descr]);
	} elsif (/^\*\s+(.*)\s*$/) {
	    my ($sect_name) = ($1);
	    if (%{$section}) {
		$section->{"commands"} = [ @commands ];
		push(@sections, $section);
		$section = {};
		@commands = ();
	    }
	    $section->{"name"} = $sect_name;
	    #print "\nSECTION: $sect_name\n\n";
	} else {
	    #print "UNHANDLED\n$_\n";
	}
    }
    if (!(@sections && ($sections[$#sections-1]) && ($sections[$#sections-1] == $section))) {
	$section->{"commands"} = [ @commands ];
	push(@sections, $section);
    }
    close(HELP);
    return \@sections;
}


########################################################################
# print_command_overview($fh, $tlacmd, $sections)
#
# Print the outline

sub print_command_overview() {
    my ($fh, $tlacmd, $sections) = (@_);
    print $fh ".SH \"COMMAND OVERVIEW\"\n";
    if ($sections && (@{$sections})) {
	my $section;
	foreach $section (@{$sections}) {
	    my $sname = $section->{"name"};
	    $sname =~ s/^help$/Help/g;
	    print $fh ".SS \"", &man_escape($sname), "\"\n";
	    my $command;
	    foreach $command (@{$section->{"commands"}}) {
		my $cmd = $command->[0];
		my $descr = $command->[1];
		#print "    ", $command->[0], "\n";
		#print "        ", $command->[1], "\n";
		my $usage = "$tlacmd $cmd [options] [...]";
		open(HELP, "$tlacmd $cmd -h 2>&1 |")
		    or die "Cannot run \`$tlacmd $cmd -h'! $!";
		$_ = <HELP>;
		if ($_) {
		    chomp;
		    $descr = $_;
		    $_ = <HELP>;
		    if ($_) {
			chomp;
			if (/^usage:\s+(.*)\s*$/) {
			    $usage = $1;
			}
		    }
		}
		close(HELP);
		$command->[2] = $usage;
		print($fh ".TP\n.B \"", &man_escape($usage), 
		      "\"\n", &man_escape($descr), "\n\n");
		#print "        usage: ", $usage, "\n";
	    }
	}
    } else {
	#print "No sections found.\n";
	return undef;
    }
}


########################################################################
# print_command_details($fh, $tlacmd, $command)
#
# Print the command details

sub print_command_details() {
    my ($fh, $tlacmd, $command, $print_common_options) = (@_);
    my $cmd = $command->[0];
    my $descr = $command->[1];
    open(DETAILS,"$tlacmd $cmd -H 2>&1 |")
	or die "Cannot run \`$tlacmd $cmd -H'! $!";
    my $state = 0;
    my @textlines = ();
    my $line;
    while (<DETAILS>) {
	chomp;
	$line = $_;
	if ($state == 0) {
	    $state++;
	} elsif ($state == 1) {
	    die "Unknown output format of \`$tlacmd $cmd -H'"
		unless ($line =~ /^usage:\s+/);
	    $state++;
	} elsif ($state >= 2) {
	    my $newstate;
	    if ($line =~ /^$/) {
		# empty line
		$newstate = 2;
	    } elsif ($line =~ /^\s+--?/) {
		# line is a parameter description
		$newstate = 3;
	    } elsif ($line =~ /^\s+/) {
		# indented line
		$newstate = 4;
	    } elsif ($line =~ /^([A-Z][a-zA-Z-]+:)\s(\[.*)$/) {
		# Grab file syntax
		$line = sprintf("  %-17s %s", $1, $2);
		$newstate = 6;		
	    } else {
		# text line
		push(@textlines, $line);
		$newstate = 5;
	    }
	    if (($state == 5) && ($newstate != 5)) {
		print $fh ".PP\n", &man_escape(join(' ',@textlines)), "\n";
		@textlines = ();
	    }
	    if (($state == 3) && ($line =~ /^\s+and exit.$/)) {
		# ignore common param descriptions for -h,-H,-V if cmd!='help'
		if ($print_common_options || ($cmd eq 'help')) {
		    print $fh &man_escape($line), "\n";
		}
	    } elsif ($newstate == 3) {
		if ((!$print_common_options) &&
		    ($cmd ne 'help') &&
		    ($line =~ /^\s+-h, --help\s+Display a help message and exit.$/ || 
		     $line =~ /^\s+-H\s+Display a verbose help message and exit.$/ ||
		     $line =~ /^\s+-V, --version\s+Display a release identifier string$/ ||
		     $line =~ /^\s+-V, --version\s+Display a release identifier string and exit./ ||
		     $line =~ /^\s+-h, --help\s+display help$/ ||
		     $line =~ /^\s+-V, --version\s+display version info$/)) {
		    # ignore common param descriptions for -h,-H,-V if cmd!='help'
		    # These commands need extra treatment and force us to use
		    # that many regexps:
		    #   baz 1.2
		    #      diff -V
		    #      inventory -h, -V
		    #      status -V
		    #   tla 1.3
		    #      inventory -h, -V
		} else {
		    print $fh &man_escape($line), "\n";
		}
	    } elsif (($newstate == 4) || ($newstate == 6)) {
		print $fh &man_escape($line), "\n";
	    } elsif ($newstate == 2) {
		print $fh "\n";
	    }
	    $state = $newstate;
	}
    }
    if ($state == 5) {
	print $fh ".PP\n", &man_escape(join(' ',@textlines)), "\n";
    }
    close(DETAILS);
}


########################################################################
# print_all_details($fh, $tlacmd, $sections)
#
# Print the command details

sub print_all_details() {
    my ($fh, $tlacmd, $sections, $print_common_options) = (@_);
    if ($sections && (@{$sections})) {
	my $section;
	foreach $section (@{$sections}) {
	    my $sname = $section->{"name"};
	    print $fh ".SH \"", &man_escape(uc($sname)), "\"\n";
	    my $command;
	    foreach $command (@{$section->{"commands"}}) {
		my $cmd   = &man_escape($command->[0]);
		my $descr = &man_escape($command->[1]);
		my $usg   = &man_escape($command->[2]);
		print $fh '.SS "', &man_escape($tlacmd), ' ', $cmd, "\"\n";
		print $fh '.B "', $descr, "\"\n";
		print $fh ".PP\n.B \"Usage:\"\n", $usg, "\n";
		&print_command_details($fh, $tlacmd, $command, 
				       $print_common_options);
	    }
	}
    } else {
	print "No sections found.\n";
	return undef;
    }
}


########################################################################
# print_head($fh, $tlacmd, $version)
#
# Print man page head

sub print_head() {
    my ($fh, $tlacmd, $version) = (@_);
    my $tm = time();
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) =	gmtime($tm);
    my $datestamp = sprintf("%04d-%02d-%02d", 1900+$year, $mon, $mday);
    my $timestamp = scalar gmtime($tm);
    my $common_head_str = <<ENDOFHEAD;
.\\\" Man page for $tlacmd
.\\\"
.\\\" Large parts of this file are autogenerated from the output of
.\\\"     "$tlacmd help"
.\\\"     "$tlacmd <cmd> -h"
.\\\"     "$tlacmd <cmd> -H"
.\\\"
.\\\" Other parts were written for Debian Bug #201172 by Loic Minier,
.\\\" based on the the "arch Meets hello-world" tutorial
.\\\" which is Copyright (C) 2001, 2002, 2003 Thomas Lord.
.\\\"
.\\\" Other parts were written for Debian Bug #201172 by Hans Ulrich Niedermann
.\\\"
.\\\" Generation time: $timestamp
.\\\"
ENDOFHEAD
    my $tla_str = <<ENDOFHEAD;
.TH $tlacmd 1 "$datestamp" "$version" "$tlacmd arch client"
.SH "NAME"
$tlacmd \- arch command line client tool
.SH "SYNOPSIS"
.B "$tlacmd"
.I "command"
[
.I "command_options"
]
.br
.B "$tlacmd"
.I "command"
[-h|--help|-H]
.br
.B "$tlacmd"
[-h|--help|-H|-V|--version]
.SH "DESCRIPTION"
.B "$tlacmd"
is an implementation of
.B "arch".

.B "arch"
is a version control system, which allows you to keep old versions of files and directories (usually source code), keep a log of who, when, and why changes occurred, etc., like SVN, CVS, or RCS.

.B "arch"
has a number of advantages compared to competing systems. Among these are:
 
.SS "Works on Whole Trees"
.SP
.B "arch"
keeps track of whole trees -- not just individual files.
For example, if you change many files in a tree,
.B "arch"
can record all of those changes as a group rather than file-by-file;
if you rename files or reorganize a tree,
.B "arch"
can record those tree arrangements along with your changes to file contents.

.SS "Changeset Oriented"
.SP
.B "arch"
doesn\'t simply "snapshot" your project trees.
Instead,
.B "arch"
associates each revision with a particular changeset:
a description of exactly what has changed.
.B "arch"
provides changeset oriented commands to help you review changesets, merge trees by applying changesets, examine the history of a tree by asking what changesets have been applied to it, and so forth.

.SS "Fully Distributed"
.SP
.B "arch"
doesn\'t rely on a central repository.
For example, there is no need to give write access to a project\'s archive to all significant contributors. Instead, each contributor can have their own archive for their work.
.B "arch"
seamlessly operates across archive boundaries.
ENDOFHEAD
#.SH "EXAMPLES"
    print $fh &man_escape($common_head_str);
    print $fh &man_escape($tla_str);
}


########################################################################
# print_foot($fh, $tlacmd)
#
# Print man page foot

sub print_foot() {
    my ($fh, $tlacmd) = (@_);
#.SH "EXIT STATUS"
#.TP
#.I "0"
#Successful program execution
#.TP
#.I "1"
#Something (bad?) happened.
#.TP
#.I "2"
#Something (bad?) happened.
#.TP
#.I "other"
#Something (bad?) happened.
# According to 'rgrep getenv bazaar/src', these env vars are used:
#.SH "ENVIRONMENT"
#EDITOR
#HOME
#http_proxy
#HTTP_PROXY
#TMPDIR
    my $str = <<ENDOFFOOT;
.SH "ENVIRONMENT"
.TP
.I "EDITOR"
If
.RB \$ EDITOR
is set, use its value as the path of the text editor
.B "arch"
is to run when asking the user for text input. If unset, log messages must be given on the command line using the \`-L\'
parameter or in the file created by \`$tlacmd make-log\'.
.TP
.I "HOME"
User\'s home directory, where
.B "arch"
looks for
.I ".arch-cache/"
and
.I ".arch-params/" .

.TP
.I "http_proxy HTTP_PROXY"
If
.RB \$ http_proxy
or
.RB \$ HTTP_PROXY
is set,
.B "arch"
used its value as the URL of the proxy to use for WebDAV accesses.
.RB \$ http_proxy
has higher priority than
.RB \$ HTTP_PROXY .
If unset, no proxy is used.
.TP
.I "TMPDIR"
If
.RB \$ TMPDIR
is set,
.B "arch"
creates temporary files in the given directory. Otherwise, it uses \`/tmp\'.
.SH "FILES"
.TP
.I "\${HOME}/.arch-cache/"
Directory where
.B "arch"
caches archive data
.TP
.I "\${HOME}/.arch-params/"
Directory where all the user\'s settings are stored.
.TP
.I "\${HOME}/.arch-params/hook"
Hook script called after every execution of $tlacmd.
.TP
.I "\${HOME}/.arch-params/signing/"
Directory where the commands for signing and checking signatures are stored.
ENDOFFOOT
    print $fh &man_escape($str);
    my $refs;
    if ($tlacmd =~ /baz$/) {
	$refs = [ "http://bazaar.canonical.com/", 
		  "http://wiki.gnuarch.org/",
		  "http://gnuarch.org/",
		  ];
    } else {
	$refs = [ "http://gnuarch.org/", 
		  "http://wiki.gnuarch.org/",
		  ];
    }
    &print_see_also($fh, $tlacmd, $refs);
}


########################################################################
# print_see_also ($fh, $tla_cmd, $references)

sub print_see_also() {
    my ($fh, $tlacmd, $references) = (@_);
    sub reffmt() {
	my ($ref) = (@_);
	if ($ref =~ m|^http://|) {
	    return ".UR $ref\n.BR $ref";
	} elsif ($ref =~ m|^([a-z0-9_+-]+)\((\d+)\)$|) {
	    my ($mp,$sn) = ($1,$2);
	    return ".BR $mp ($sn)";
	} else {
	    return $ref;
	}
    }
    print $fh ".SH \"SEE ALSO\"\n";
    print $fh &man_escape(join(",\n", map({ &reffmt($_); } @{$references})));
}


########################################################################
# generate_manpage($tla_cmd, $filename)

sub generate_manpage() {
    my ($manpage, $print_common_options) = (@_);
    my $filename = $manpage;
    my ($tlacmd, $mansect, $mansectcompl);
    if ($manpage =~ /^(.*)\.(([0-9]+)[a-z]*)$/) {
	$tlacmd = $1;
	$mansectcompl = $2;
	$mansect = $3;
    } else {
	die "Cannot parse man page name \`$manpage'";
    }
    if ($tlacmd =~ /baz/) {
	print(STDERR
	      "WARNING: The static text for baz.1 is the very same as for tla.1!\n");
    }

    $filename = 'debian/tmp/' . $filename;

    my $sections = &build_section_list($tlacmd);

    # Check that $tlacmd is executable
    open(VERSION,"$tlacmd --version |")
	or die "Cannot run \`$tlacmd --version'! $!";
    $_ = <VERSION>;
    my $version;
    if ($_) {
	chomp;
	if (/^tla tla-([^\s]+) from regexps.com$/) {
	    $version = $1; # tla style
        } elsif (/^tla-([^\s]+)$/) {
            $version = $1; # debian style
	} elsif (/^baz Bazaar version ([^\s]+)/) {
	    $version = $1; # baz style
	} elsif (/^The GNU Arch Revision Control System \(tla\) (\S+)/) {
	    $version = $1; # GNU Arch style
	} else {
	    die "Don't know how to parse \`$tlacmd --version' message: $_";
	}
    }
    close(VERSION);

    print STDERR "Generating manpage for \`$tlacmd'...";
    open my $fh, ">$filename" 
	or die "Cannot open $filename! $!";

    &print_head($fh, $tlacmd, $version);
    &print_command_overview($fh, $tlacmd, $sections);
    &print_all_details($fh, $tlacmd, $sections, $print_common_options);
    &print_foot($fh, $tlacmd);

    close($fh);
    print STDERR " done.\n";
}


########################################################################
# Main program

my @manpages;
my $print_common_options = (1 == 1);

my $arg;
foreach $arg (@ARGV) {
    if ($arg eq '-h' || $arg eq '--help') {
	print "Syntax: generate-manpage.pl [<tla.1>|<baz.1>]...\n";
	exit(0);
    } elsif ($arg eq '-V' || $arg eq '--version') {
	print "unknown\n";
	exit(0);
    } elsif ($arg eq '--no-common') {
	print "Generating man page(s) without common options\n";
	$print_common_options = (1 == 0);
    } elsif ($arg =~ /^([A-Za-z_-]+\.[0-9]+[a-zA-Z]*)$/) {
	# name of man page to generate, add it to list
	push(@manpages, $1);
    } else {
	die "Unrecognized argument: $arg";
    }
}
if ($#manpages < 0) {
    # No man pages given on command line, so default to these:
    @manpages = ("tla.1", "baz.1");
}

my $manpage;
foreach $manpage (@manpages) {
    &generate_manpage($manpage,$print_common_options);
}

# arch-tag: 5fac2ad5-576b-4461-ba37-4f953e96e9d2
