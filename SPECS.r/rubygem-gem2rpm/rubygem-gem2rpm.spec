# Generated from gem2rpm-0.5.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name gem2rpm

Name: rubygem-%{gem_name}
Version: 0.11.2
Release: 2%{?dist}
Summary: Generate rpm specfiles from gems
Group: Development/Languages
License: GPLv2+
URL: https://github.com/fedora-ruby/gem2rpm
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/fedora-ruby/gem2rpm.git && cd gem2rpm && git checkout v0.11.2
# tar czvf gem2rpm-0.11.2-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
Requires: %{_bindir}/rpmdev-packager
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: %{_bindir}/rpmdev-packager
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Generate source rpms and rpm spec files from a Ruby Gem.  The spec file
tries to follow the gem as closely as possible, and be compliant with the
Fedora rubygem packaging guidelines.


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

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

# Disable this test, since it needs online access (see the comment on line 22).
sed -i "/test_find_download_url_for_source_address/,/  end/ s/^/#/" test/test_gem2rpm.rb

ruby -Itest -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/gem2rpm
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%{gem_instdir}/templates
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/README.md

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.11.2-2
- 为 Magic 3.0 重建

* Mon Aug 17 2015 Vít Ondruch <vondruch@redhat.com> - 0.11.2-1
- Update to gem2rpm 0.11.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Vít Ondruch <vondruch@redhat.com> - 0.11.1-1
- Update to gem2rpm 0.11.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Vít Ondruch <vondruch@redhat.com> - 0.10.1-1
- Update to gem2rpm 0.10.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Vít Ondruch <vondruch@redhat.com> - 0.9.2-1
- Update to gem2rpm 0.9.2.

* Mon Apr 22 2013 Vít Ondruch <vondruch@redhat.com> - 0.9.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to gem2rpm 0.9.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 09 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.1-1
- Fix template for F17 and above.
- Fix release enumeration logic.

* Mon Jan 23 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.0-1
- Updated to gem2rpm 0.8.0.

* Fri Jan 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.1-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Vít Ondruch <vondruch@redhat.com> - 0.7.1-2
- gem2rpm requires rpmdev-packager tool to work properly.

* Thu Jun 30 2011 Vít Ondruch <vondruch@redhat.com> - 0.7.1-1
- Updated to the 0.7.1 version.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 28 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.6.0-5
- Breaking into a main and doc package

* Tue Nov 24 2009 David Lutterkort <lutter@redhat.com> - 0.6.0-4
- Add gemdocdir contents as doc

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct  6 2008 David Lutterkort <dlutter@redhat.com> - 0.6.0-1
- New version

* Tue Mar 11 2008 David Lutterkort <dlutter@redhat.com> - 0.5.3-1
- Bring in accordance with Fedora guidelines

* Thu Jan  3 2008 David Lutterkort <dlutter@redhat.com> - 0.5.2-2
- Own geminstdir
- Fix Source URL

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 0.5.1-1
- Initial package
