%global gem_name xmlparser

Summary: Ruby bindings to the Expat XML parsing library
Name: rubygem-%{gem_name}
Version: 0.7.2.1
Release: 15%{?dist}
Group: Development/Languages
# src/lib/xml/xpath.rb is GPLv2+
# src/ext/encoding.h and the functions of encoding map are GPLv2+ or Artistic
# All other files are Ruby or GPLv2+ or MIT
# For a breakdown of the licensing, see also README
License: GPLv2+ and ( Ruby or GPLv2+ or MIT ) and ( GPLv2+ or Artistic ) 
URL: http://rubygems.org/gems/xmlparser
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
# Handle 'format not a string literal and no format arguments' error.
# https://bugzilla.redhat.com/show_bug.cgi?id=1037312
# Thanks to Gregor Herrmann for the patch.
# https://www.mail-archive.com/debian-bugs-rc@lists.debian.org/msg297233.html
Patch0: rubygem-xmlparser-ftbfs-fix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ruby
BuildRequires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
BuildRequires: rubygem(rake)
BuildRequires: rubygem(mkrf)
BuildRequires: expat-devel

%description
Ruby bindings to the Expat XML parsing library. 

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%patch0 -p1

%build
gem build %{gem_name}.gemspec
%gem_install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -rp .%{gem_dir}/* %{buildroot}%{gem_dir}/

# remove development stuff
rm -rf %{buildroot}%{gem_instdir}/ext

# install externals
mkdir -p %{buildroot}%{gem_extdir_mri}/
cp -a ./%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/


%files
%{gem_extdir_mri}
%dir %{gem_instdir}/
%doc %{gem_instdir}/[A-Z]*
%doc %{gem_docdir}
%{gem_instdir}/[a-z]*
%exclude %{gem_cache}
%{gem_spec}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.7.2.1-15
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.7.2.1-14
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.2.1-13
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 0.7.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Fix FTBFS if "-Werror=format-security" flag is used (rhbz#1037312).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.2.1-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.7.2.1-3
- sync with updated gem version from rubyforge instead of private copy
- use macros for files section
- cleanup macros in changelog section to make rpmlint happy

* Wed Apr 25 2012 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.7.2-2
- use macros following the new gem packaging guidelines for fed17+

* Tue Mar 20 2012 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.7.2-1
- spec file patch to support fedora 17+
- update to 0.7.2 from Yoshidam

* Tue Mar 06 2012 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-9
- replace build requirement for ruby-libs by ruby 

* Wed Dec 07 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-8
- remove the link to xmlparser.so and move it to ruby_sitearch

* Wed Dec 07 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-7
- fix for /usr/lib/ruby/gems/1.8/gems/xmlparser-0.6.81 should be owned by the package
- fix installation path for .so files
- add dependency on ruby-libs which owns the ruby_sitearch directory

* Wed Jul 12 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-6
- add more details about licensing

* Wed Jul 12 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-5
- specify
- fix format of changelog
- remove ruby-sitelib

* Tue Jul 11 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-4
- cleaner way to treat SOURCE
- remove explicit dependency on expat
- make globals conditional

* Mon Jul 10 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-3
- fix build problems 

* Sat Jul 08 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-2
- add dependencies

* Wed Jul 06 2011 Ulrich Schwickerath <ulrich.schwickerath@web.de> - 0.6.81-1
- Initial package from gem2rpm

