%global gem_name formatador

%global bootstrap 0

Summary: Ruby STDOUT text formatting
Name: rubygem-%{gem_name}
Version: 0.2.4
Release: 7%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/geemus/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
%if 0%{bootstrap} < 1
BuildRequires: rubygem(shindo)
%endif
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
STDOUT text formatting

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%check
%if 0%{bootstrap} < 1
pushd .%{gem_instdir}
# if we don't use -Ilib, the already installed (perhaps older) gem will be used
# but we want to test the actually packaged
RUBYOPT=-Ilib shindo
popd
%endif

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.rdoc
%{gem_libdir}
%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/changelog.txt
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/tests
%{gem_instdir}/formatador.gemspec

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.4-4
- Enable tests again.

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.4-1
- Update to 0.2.4.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.1-4
- Set %%bootstrap to 0 to allow tests.

* Wed Jan 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.1-3
- Rebuilt for Ruby 1.9.3.
- Added %%bootstrap macro for tests.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.1-1
- Update to 0.2.1
- Added check section
- Introduced doc subpackage
- Added tests patch for the case when output is redirected to a file (would fail in mock and koji)

* Thu Jul 21 2011 Chris Lalancette <clalance@redhat.com> - 0.1.4-2
- Remove bogus shindo and rake dependencies

* Tue Jul 05 2011 Chris Lalancette <clalance@redhat.com> - 0.1.4-1
- Initial package
