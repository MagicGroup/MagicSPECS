# Generated from rails-1.2.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails


Summary: Web-application framework
Name: rubygem-%{gem_name}
Epoch: 1
Version: 4.2.4
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: http://rubygems.org/downloads/rails-%{version}.gem

BuildRequires: rubygems-devel

BuildArch: noarch

%description
Rails is a framework for building web-application using CGI, FCGI, mod_ruby,
or WEBrick on top of either MySQL, PostgreSQL, SQLite, DB2, SQL Server, or
Oracle with eRuby- or Builder-based templates.

%package doc
Summary: Documentation for %{name}
Group: Documentation
# SyntaxHighlighter is dual licensed under the MIT and GPL licenses
License: MIT and (MIT or GPL+)
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
This package contains documentation for %{name}.


%prep

%build

%install
%gem_install -n %{SOURCE0}

mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_spec}
%exclude %{gem_cache}
%exclude %{gem_docdir}

%files doc
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/guides

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1:4.2.4-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1:4.2.4-2
- 为 Magic 3.0 重建

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.4-1
- Update to rails 4.2.4

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.3-1
- Update to rails 4.2.3

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.2-1
- Update to rails 4.2.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.1-1
- Update to rails 4.2.1

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.0-1
- Update to rails 4.2.0

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 4.1.5-1
- Update to rails 4.1.5

* Fri Jul 04 2014 Josef Stribny <jstribny@redhat.com> - 4.1.4-1
- Update to rails 4.1.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.1-1
- Update to Rails 4.1.1

* Thu Apr 24 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Apr 15 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.0-1
- Update to Rails 4.1.0

* Tue Apr 08 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.3-2
- Own %%{gem_instdir}
  - Resolves: rhbz#1085198

* Wed Feb 26 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.3-1
- Update to Rails 4.0.3

* Wed Feb 05 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-2
- Fix license in -doc subpackage

* Thu Dec 05 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-1
- Update to Rails 4.0.2

* Thu Nov 14 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.1-1
- Update to Rails 4.0.1.

* Mon Aug 12 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.0-2
- Fix: -doc subpackage requires

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.0-1
- Update to Rails 4.0.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.13-1
- Updated to Rails 3.2.13.

* Sat Mar 09 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Feb 12 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-1
- Updated to Rails 3.2.12.

* Wed Jan 09 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.11-1
- Updated to Rails 3.2.11.

* Fri Jan 04 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.10-1
- Updated to Rails 3.2.10.

* Mon Aug 13 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.8-1
- Updated to Rails 3.2.8.

* Mon Jul 30 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.7-1
- Updated to Rails 3.2.7.

* Fri Jul 27 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.2.6-1
- Updated to Rails 3.2.6.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.15-1
- Update to Rails 3.0.15.

* Fri Jun 01 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.13-1
- Update to Rails 3.0.13.

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-1
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.10-1
- Update to Rails 3.0.10

* Thu Jul 07 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.9-1
- Update to Rails 3.0.9

* Tue Mar 29 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.5-2
- Cleanup

* Tue Mar 29 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.5-1
- Updated to Rails 3.0.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Mohammed Morsi <mmorsi@redhat.com> - 1:3.0.3-1
- Update to rails 3

* Mon Aug 09 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Sun Sep 20 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4

* Fri Jul 31 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.3-2
- Restore some changes

* Sun Jul 26 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.3-1
- New upstream version

* Wed Jul 24 2009 Scott Seago <sseago@redhat.com> - 2.3.2-3
- Remove the 'delete zero length files' bit, as some of these are needed.

* Wed May  6 2009 David Lutterkort <lutter@redhat.com> - 2.3.2-2
- Fix replacement of shebang lines; broke scripts/generate (bz 496480)

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 David Lutterkort <lutter@redhat.com> - 2.2.2-1
- New version

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-2
- require rubygems >= 1.1.1; the rails code checks that at runtime

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-1
- New version (fixes CVE-2008-4094)

* Thu Jul 31 2008 Michael Stahnke <stahnma@fedoraproject.org> - 2.1.0-1
- New Upstream

* Tue Apr  8 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-2
- Fix dependency

* Mon Apr 07 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-1
- New version

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 2.0.1-1
- New version
- No dependency on actionwebservce anymore, depend on activeresource instead

* Thu Nov 29 2007 David Lutterkort <dlutter@redhat.com> - 1.2.6-1
- Don't copy files into _docdir, mark them as doc in the geminstdir

* Tue Nov 13 2007 David Lutterkort <dlutter@redhat.com> - 1.2.5-2
- Fix buildroot

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.2.5-1
- Initial package
