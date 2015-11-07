%global gem_name sinatra

%global bootstrap 0

Summary:        Ruby-based web application framework
Name:           rubygem-%{gem_name}
Version:        1.4.6
Release:        4%{?dist}
Group:          Development/Languages
License:        MIT
URL: http://www.sinatrarb.com/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:  rubygems-devel
%if 0%{bootstrap} < 1
BuildRequires:  rubygem(rack) >= 1.4.0
BuildRequires:  rubygem(rack-test)
BuildRequires:  rubygem(rack-protection) >= 1.4.0
BuildRequires:  rubygem(tilt) >= 1.3
BuildRequires:  rubygem(tilt) < 3
BuildRequires:  rubygem(minitest) > 5
%endif
BuildArch:      noarch
Epoch:          1

%description
Sinatra is a DSL intended for quickly creating web-applications in Ruby
with minimal effort.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation

Requires:	%{name} = %{epoch}:%{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%check
%if 0%{bootstrap} < 1
pushd .%{gem_instdir}
# TODO: Is it worth of testing all the possible template engines integration?
ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd
%endif

%install
mkdir -p %{buildroot}%{gem_dir}
cp -rv .%{gem_dir}/* %{buildroot}%{gem_dir}
rm %{buildroot}/%gem_instdir/.yardopts # Remove YARD configuration

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/sinatra.gemspec
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/README.*.md
%doc %{gem_instdir}/AUTHORS.md
%doc %{gem_instdir}/CHANGES
%{gem_instdir}/examples
%{gem_instdir}/Gemfile

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1:1.4.6-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1:1.4.6-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Josef Stribny <jstribny@redhat.com> - 1:1.4.6-1
- Update to 1.4.6

* Fri Jul 18 2014 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-1
- Update to Sinatra 1.4.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Michal Fojtik <mfojtik@redhat.com> - 1:1.4.3-1
- Update to 1.4.3

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.5-1
- Update to version 1.3.5.
- Run tests again.

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.4-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 25 2013 Michal Fojtik <mfojtik@redhat.com> - 1;1.3.4-3
- Rebuild using new rack-protection

* Thu Feb 21 2013 Michal Fojtik <mfojtik@redhat.com> - 1;1.3.4-2
- Fixed rack-protection version

* Thu Feb 21 2013 Michal Fojtik <mfojtik@redhat.com> - 1;1.3.4-1
- Release 1.3.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.2-8
- Set %%bootstrap to 0 to allow tests.

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.3.2-7
- Rebuilt for Ruby 1.9.3.
- Introduced %%bootstrap macro to deal with dependency loop.

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-6
- Fixed Epoch once again

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-5
- Added Epoch to -dc subpackage

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-4
- Rebuild for missing -dc subpackage

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-3
- Added missing build requires

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-2
- Added tests
- Added doc subpackage

* Mon Jan 02 2012 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-2
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.6-1
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.0-1
- Version bump

* Thu Feb 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-3
- Added tilt dependency

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-1
- Version bump

* Thu Mar 25 2010 Michal Fojtik <mfojtik@redhat.com> - 1.0-1
- Sinatra now uses Tilt for rendering templates
- New helper methods
- New argument to specify the address to bind to
- Speed improvement in rendering templates

* Mon Feb 15 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.4-2
- Downgrade-Release

* Thu Jan 07 2010 Michal Fojtik <mfojtik@redhat.com> - 0.10.1-1
- Version-Release
- Added jp README

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-2
- Fix up documentation list
- Bring tests back
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.2-1
- Package generated by gem2rpm
- Don't ship tests
- Fix up License
