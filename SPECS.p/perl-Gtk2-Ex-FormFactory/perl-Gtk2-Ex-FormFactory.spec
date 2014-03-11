Name:           perl-Gtk2-Ex-FormFactory
Version:        0.67
Release:        3%{?dist}
Summary:        Framework for Gtk2 perl applications

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.exit1.org/Gtk2-Ex-FormFactory/
Source0:        http://www.exit1.org/packages/Gtk2-Ex-FormFactory/dist/Gtk2-Ex-FormFactory-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Gtk2)
BuildRequires:  perl(Test::More)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Gtk2::Ex::FormFactory is a framework for Perl Gtk2 developers.

%prep
%setup -q -n Gtk2-Ex-FormFactory-%{version}
# Make it so that the .pl scripts in %%doc don't add bogus requirements
chmod -x examples/* tutorial/*
# Convert encoding
for f in $(find lib/ -name *.pm) README tutorial/README; do
cp -p ${f} ${f}.noutf8
iconv -f ISO-8859-1 -t UTF-8 ${f}.noutf8 > ${f}
touch -r ${f}.noutf8 ${f}
rm ${f}.noutf8
done

# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/^perl(Music/d'

EOF

%define __perl_provides %{_builddir}/Gtk2-Ex-FormFactory-%{version}/%{name}-prov
chmod +x %{name}-prov


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

chmod 644 $RPM_BUILD_ROOT%{_mandir}/man3/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes examples/ LICENSE README tutorial/
%{perl_vendorlib}/Gtk2/
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.67-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.67-2
- 为 Magic 3.0 重建

* Tue Jan 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.67-1
- Update to 0.67

* Tue Jan 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.65-12
- Add missing BR Test::More

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.65-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.65-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.65-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.65-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.65-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.65-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.65-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.65-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 29 2008 kwizart < kwizart at gmail.com > - 0.65-3
- Fix non-utf8 encoding at source.

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 0.65-2
- Fix man3 encoding
- Fix unwanted perl provides (Music::*)

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 0.65-1
- Update to 0.65
- Fix encoding

* Mon Jan  9 2006 Matthias Saou <http://freshrpms.net/> 0.59-1
- Initial RPM package.
