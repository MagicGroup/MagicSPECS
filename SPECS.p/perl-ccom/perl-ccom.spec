# Filter the Perl extension module
%{?perl_default_filter}

Summary: 	Perl module for context-sensitive phonetic string replacement
Summary(zh_CN.UTF-8): 上下文相关的语音字符串替换的 Perl 模块
Name: 		perl-ccom
Version: 	1.4.1
Release: 	15%{?dist}
License: 	LGPLv2+
Group: 		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: 		http://www.heise.de/ct/ftp/99/25/252/
Source:		ftp://ftp.heise.de/pub/ct/listings/phonet.tgz
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A perl module for context-sensitive phonetic string replacement to modify
strings according to predefined replacement rules in such a way that words
with the same pronunciation (e.g. "tail" and "tale") are converted to the
same string. This can, for example, be used to implement error-tolerant
search routines in address databases. It contains phonetic rules for German
only, but the software has been prepared for multi-language support.
                                                                                                        
%description -l zh_CN.UTF-8
上下文相关的语音字符串替换的 Perl 模块。

%prep

%setup -q -c -n %{name}

# Clean the strange packaging first
mv -f ccom*/* .
chmod 644 *.xs ccomlib/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

# Change man page encoding into UTF-8
iconv -f latin1 -t utf-8 -o blib/man3/ccom.3pm.utf8 blib/man3/ccom.3pm
mv -f blib/man3/ccom.3pm.utf8 blib/man3/ccom.3pm

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# Fix incorrect permissions
chmod 644 Changes readme_perl.txt ccom_test.pl

# Fix incorrect end-of-line encoding
sed -e 's/\r//' -i copying.lib -i readme_perl.txt

# Fix incorrect interpreter path
sed -e 's@#! /opt/perl5/bin/perl@#!%{_bindir}/perl@' -i ccom_test.pl

# Remove test/example from regulars
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/ccom_test.pl
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Changes copying.lib readme_perl.txt ccom_test.pl
%{_mandir}/man3/*.3pm*
%{perl_vendorarch}/*.pm
%{perl_vendorarch}/auto/ccom
%{perl_vendorarch}/*.pm

%changelog
* Fri May 08 2015 Liu Di <liudidi@gmail.com> - 1.4.1-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.4.1-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.4.1-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.4.1-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.4.1-11
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.1-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4.1-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4.1-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.4.1-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.4.1-3
- Rebuild against gcc 4.4 and rpm 4.6

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.1-2
- Rebuild for new perl

* Thu Jan 31 2008 Robert Scheck <robert@fedoraproject.org> 1.4.1-1
- Upgrade to 1.4.1
- Initial spec file for Fedora and Red Hat Enterprise Linux
