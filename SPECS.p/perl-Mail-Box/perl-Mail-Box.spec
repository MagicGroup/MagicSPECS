Name:           perl-Mail-Box
Version:        2.097
Release:        5%{?dist}
Summary:        Manage a mailbox, a folder with messages
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Mail-Box/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MARKOV/Mail-Box-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker), perl(IO::Handle), perl(Scalar::Util)
BuildRequires:  perl(Encode), perl(Mail::Transport::Dbx)
# Can't have a BR on perl(Mail::Box::Parser::C), it requires perl-Mail-Box (whoops)
BuildRequires:  perl(Mail::IMAPClient), perl(Mail::Internet)
BuildRequires:  perl(MIME::Entity), perl(HTML::TreeBuilder), perl(Time::HiRes)
BuildRequires:  perl(HTML::FormatText), perl(Date::Parse), perl(File::Spec), perl(File::Remove)
BuildRequires:  perl(Errno), perl(Object::Realize::Later), perl(Mail::Address), perl(MIME::Types)
BuildRequires:  perl(Sys::Hostname), perl(Test::More), perl(Test::Harness), perl(MIME::Base64)
BuildRequires:  perl(URI), perl(IO::Scalar), perl(Digest::HMAC_MD5), perl(User::Identity)
BuildRequires:  perl(Time::Zone), perl(Email::Simple), perl(Text::Autoformat)
BuildRequires:  perl(Email::Abstract)
# When perl(TAP::Harness) shows up, uncomment this, and re-enable the tests.
BuildRequires:  perl(TAP::Harness)
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# I'm not sure why these provides aren't getting picked up automatically.
Provides: perl(Mail::Message::Body::Construct) = %{version}
Provides: perl(Mail::Message::Construct) = %{version}
Provides: perl(Mail::Message::Construct::Bounce) = %{version}
Provides: perl(Mail::Message::Construct::Build) = %{version}
Provides: perl(Mail::Message::Construct::Forward) = %{version}
Provides: perl(Mail::Message::Construct::Read) = %{version}
Provides: perl(Mail::Message::Construct::Rebuild) = %{version}
Provides: perl(Mail::Message::Construct::Reply) = %{version}
Provides: perl(Mail::Message::Construct::Text) = %{version}

# I'm also not sure why this requirement isn't getting picked up automatically.
Requires: perl(Object::Realize::Later)

%description
The Mail::Box folder is a modern mail-folder manager -- at least at
the moment of this writing ;)  It is written to replace Mail::Folder,
although its interface is different.

%prep
%setup -q -n Mail-Box-%{version}

%filter_from_requires /perl(Mail::SpamAssassin)/d
%{?perl_default_filter}


%build
yes y |%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
# Nuke Zero length files
rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/Mail/Box-Overview.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/Mail/Box-Cookbook.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/Mail/Box-Index.pod
# Fix file encoding
recode()
{
        iconv -f "$2" -t utf-8 < "$1" > "${1}_"
        mv -f "${1}_" "$1"
}
recode $RPM_BUILD_ROOT%{_mandir}/man3/Mail::Message::Field.3pm iso-8859-1

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README LICENSE README.FAQ README.todo ChangeLog examples/
%{perl_vendorlib}/Mail/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.097-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.097-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.097-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.097-2
- Perl mass rebuild

* Wed Mar  2 2011 Tom Callaway <spot@fedoraproject.org> - 2.097-1
- update to 2.097
- remove Mail::SpamAssassin from BuildRequires
- filter Mail::SpamAssassin out of Requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.095-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.095-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.095-1
- update to 2.095

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.091-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.091-2
- rebuild against perl 5.10.1

* Wed Sep  9 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.091-1
- update to 2.091

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.087-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.087-1
- update to 2.087

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.084-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.084-1
- update to 2.084

* Thu Jun  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.082-1
- update to 2.082

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.073-5
- Rebuild second pass, tests enabled

* Sun Mar  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.073-4
- Rebuild, first pass, disable tests, BR on Email::Abstract

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.073-3
- Rebuild for perl 5.10 (again)

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.073-2
- rebuild for new perl

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.073-1.1
- first rebuild pass, break look with Email::Abstract

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.073-1
- 2.073
- license fix

* Wed Apr  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.070-2
- add examples/ to %%doc

* Mon Apr  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.070-1
- Initial package for Fedora
