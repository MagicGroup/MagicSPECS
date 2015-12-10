# Generated from mail-2.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mail

Name: rubygem-%{gem_name}
Version: 2.6.3
Release: 5%{?dist}
Summary: Mail provides a nice Ruby DSL for making, sending and reading emails
Group: Development/Languages
License: MIT
URL: https://github.com/mikel/mail
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/mikel/mail.git && cd mail && git checkout 2.6.3
# tar czvf mail-2.6.3-specs.tgz spec/
Source1: %{gem_name}-%{version}-specs.tgz
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: ruby
BuildRequires: rubygem(mime-types) >= 1.16
BuildRequires: rubygem(mime-types) < 3
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
A really Ruby Mail handler.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}


%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/Dependencies.txt
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/TODO.rdoc
%{gem_instdir}/Gemfile*
%{gem_instdir}/Rakefile


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.6.3-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.6.3-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.6.3-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Vít Ondruch <vondruch@redhat.com> - 2.6.3-1
- Update to Mail 2.6.3.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Vít Ondruch <vondruch@redhat.com> - 2.5.4-1
- Update to mail 2.5.4.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 2.5.3-1
- Update to Mail 2.5.3.

* Tue Mar 05 2013 Vít Ondruch <vondruch@redhat.com> - 2.4.4-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 09 2012 Vít Ondruch <vondruch@redhat.com> - 2.4.4-1
- Update to Mail 2.4.4.

* Tue Jan 31 2012 Vít Ondruch <vondruch@redhat.com> - 2.3.0-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 04 2011  <Minnikhanov@gmail.com> - 2.3.0-1
- Updated mail to latest upstream release (v.2.3.0 2011-04-27)
- Test excluded. May be need Zentest >= 4.4.0 and rubygem(rcov).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011  <Minnikhanov@gmail.com> - 2.2.15-2
- Fix Comment 18 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c18 
- Remove create Gemfile.lock at prep-section.

* Sat Jan 29 2011  <Minnikhanov@gmail.com> - 2.2.15-1
- Updated mail to latest upstream release (v.2.2.15 2011-01-25)

* Thu Jan 27 2011  <Minnikhanov@gmail.com> - 2.2.14-5
- Fix Comment 14 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c14 

* Mon Jan 24 2011  <Minnikhanov@gmail.com> - 2.2.14-4
- Fix Comment 12 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c12 

* Sun Jan 23 2011  <Minnikhanov@gmail.com> - 2.2.14-3
- 'BuildRequires:' correct wrong tag 'BuildRequires(check):'. 

* Sat Jan 22 2011  <Minnikhanov@gmail.com> - 2.2.14-2
- Fix Comment 6 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c6 

* Thu Jan 13 2011  <Minnikhanov@gmail.com> - 2.2.14-1
- Updated mail to latest upstream release

* Fri Dec 24 2010  <Minnikhanov@gmail.com> - 2.2.13-1
- Initial package

