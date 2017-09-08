#!/usr/bin/perl

#*******************************************
use warnings;
use strict;
use File::Path qw(make_path);
use CGI::Carp qw/fatalsToBrowser/;
use CGI qw/:standard/;
use lib '../lib';

require "./Abills/Templates.pm";

our %FORM;
require "./Abills/HTML.pm";
Abills::HTML->import();
use Data::Dumper;

our $html = Abills::HTML->new({});
    $html->{METATAGS} = templates('menu', {OUTPUT2RETURN => 1});
    print $html->header();

my $FROM_DIR= "/usr/abills/Abills";
my $TO_DIR= "/usr/abills/DOC";

my ($simplified_dir) = $TO_DIR =~ /(.*\/)/;
my $simplified_to_dir;


if($FORM{TREE}){
  $simplified_to_dir = $FORM{TREE};
  $simplified_to_dir =~ s/$simplified_dir//;
  print $html->tpl_show(templates('three'), {TITLE => $simplified_to_dir, OUTPUT2RETURN => 1});
  find_finished_files($FORM{TREE});
}
if($FORM{OPEN}){

my $file_name = $TO_DIR . '/' . $FORM{OPEN};
my $file_content = `perldoc -ohtml -T -F $file_name`;
if (-f $file_name && $file_name !~ m/\.\./){
  $file_name =~ s/.*\///;
  print $html->tpl_show(templates('open'), {TITLE => $file_name, FILE_CONTENT => $file_content ,OUTPUT2RETURN => 1});
  
}
else {
  print "No such file $file_name";
}

}

unless($FORM{TREE}){
  `rm -r $TO_DIR`;
  $simplified_to_dir = $TO_DIR;
  $simplified_to_dir =~ s/$simplified_dir//;
  print $html->tpl_show(templates('three'), {TITLE => $simplified_to_dir, OUTPUT2RETURN => 1});
  find_files($FROM_DIR);
  find_finished_files($TO_DIR);
}




sub parse_file {

  my ($base_dir, $fname) = @_;
  my $path_to_doc = "$base_dir";
  my $line_value = '';
  my $count      = 0;

  open(my $fh, '<', "$base_dir/$fname")
    or die "Can't open < $base_dir/$fname: $!";

  while (my $line = <$fh>) {

    if ($line =~ m/^\=head2/) {

      $count++;
    }

    $line_value .= $line if $count > 0;

    if ($line =~ m/^\=cut/) {
      $line_value .= "\n\n";
      $count = 0;
    }

  }
  close $fh;

  my $file_doc = "$fname";
  # $file_doc =~ s/.*\/(.*)\.pm$/$1\.doc/;
  $file_doc =~ s/\.pm/.pm/;
  $path_to_doc =~ s/$FROM_DIR\//$TO_DIR\//;
  open($fh, '>', "$path_to_doc/$file_doc") or die "Can't open file $path_to_doc/$file_doc : $!";
  print $fh $line_value;
  close $fh;
}

sub find_files {

  my ($base_dir) = @_;
  my $path;
  my $dir_name_for_check = $TO_DIR;
  $dir_name_for_check =~ s/.*\///;


  opendir(my $dh, $base_dir) or die "Can't opendir $base_dir: $!";

  while (my $fname = readdir $dh) {


    next if (($fname eq '.') || ($fname eq '..'));
    next if ($fname =~ m/$dir_name_for_check/);

    if (-d "$base_dir/$fname") { 
      find_files("$base_dir/$fname");
    }

    if (-f "$base_dir/$fname" && $fname =~ m/\.pm$/) {
      $path = "$base_dir/$fname";
      $path =~ s/$FROM_DIR/$TO_DIR/;
      my ($path_dir) = $path =~ /(.*\/)/; 
      `mkdir -p $path_dir`; `chmod 777 $path_dir`;
      parse_file($base_dir, $fname);
 
    }

  }
  closedir $dh;
}

sub find_finished_files {

  my ($base_dir) = @_;
  my $path;
  my @folders;
  my @files;
  $path = $base_dir;
  if($base_dir ne $TO_DIR){
    my ($path_dir) = $path =~ /(.*)\//; 
    print "<br>" . $html->button(" /.. ", "TREE=$path_dir&TITLE=$base_dir",   { class => "default", ADD_ICON => "glyphicon glyphicon-folder-open" });
  }

  
  
  opendir(my $dh, $base_dir) or die "Can't opendir $base_dir: $!";
  while (my $fname = readdir $dh) {

    next if (($fname eq '.') || ($fname eq '..'));
    if (-d "$base_dir/$fname") {
      push @folders, $html->button(" $fname", "TREE=$base_dir/$fname&TITLE=$base_dir",   { class => "default", ADD_ICON => "glyphicon glyphicon-folder-open" });
    }

    if (-f "$base_dir/$fname" && $fname =~ m/\.pm$/) {
      $path = "$base_dir/$fname";
      $path =~ s/$TO_DIR\///;
      push @files, $html->button(" $fname", "OPEN=$path&TREE=$base_dir",   { class => "default", ADD_ICON => "glyphicon glyphicon-file" });
    }

  }
  closedir $dh;

  foreach my $folder (@folders) {
    print "<br>$folder";
  }
  foreach my $file (@files) {
    print "<br>$file";
  }
}


print "</body>";
print "</html>";
