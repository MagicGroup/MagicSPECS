#!/bin/sh
exec /usr/lib/rpm/perl.req | \
        sed -e s/perl\(controllib.pl\)// | sed -e s/perl\(file\)// | sed -e s/perl\(in\)// | sed -e s/perl\(Dselect::Ftp\)// | sed -e s/perl\(extra\)//
