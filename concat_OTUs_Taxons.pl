#!/usr/bin/perl

use warnings;
use strict;

# Create a Krona input file to show metagenomic data from usearch and mapseq outputs
# OTU table should have only 2 columns: OTUs and 1 treatment.
# USAGE: perl concat_OTUs_Taxons.pl OTUtab.txt taxon.mapseq

# open files
my ($OTUtab, $taxonMAPSEQ) = @ARGV;
open (OTUTAB, "<", $OTUtab) or die $!;
my %otus_hash;

my $otutab_header = <OTUTAB>;
# fill %otushash with OTUS as keys
while (<OTUTAB>) {
	chomp;
	my @line = split /\t/, $_;
	$otus_hash{$line[0]}{coverage} = "$line[1]";
}
close OTUTAB;

open (TAXONTABLE, "<", $taxonMAPSEQ) or die $!;
my $mapseq_header1 = <TAXONTABLE>;
my $mapseq_hearder2 = <TAXONTABLE>;
while (<TAXONTABLE>) {
	chomp;
	my @line = split /\t/, $_;
	$otus_hash{$line[0]}{kingdom}=$line[13];
        $otus_hash{$line[0]}{phylum}=$line[16];
        $otus_hash{$line[0]}{class}=$line[19];
        $otus_hash{$line[0]}{order}=$line[22];
        $otus_hash{$line[0]}{family}=$line[25];
        $otus_hash{$line[0]}{genus}=$line[28];
        $otus_hash{$line[0]}{species}=$line[31];

}
close TAXONTABLE;

foreach my $otu (keys %otus_hash) {
	print "$otus_hash{$otu}{coverage}\t$otus_hash{$otu}{kingdom}\t$otus_hash{$otu}{phylum}\t$otus_hash{$otu}{class}\t$otus_hash{$otu}{order}\t$otus_hash{$otu}{family}\t$otus_hash{$otu}{genus}\t$otus_hash{$otu}{species}\n";
}

exit;
