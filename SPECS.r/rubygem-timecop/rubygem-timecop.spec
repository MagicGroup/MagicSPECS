%global gem_name timecop

Summary: Provides a unified method to mock Time.now, Date.today in a single call
Name: rubygem-%{gem_name}
Version: 0.7.1
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/travisjeffery/timecop
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
# Go with plain minitest.
# https://github.com/travisjeffery/timecop/commit/c30897f67ad90f0582c0ed0d7b78f46a7142f113
Patch0: rubygem-timecop-0.7.1-Use-minitest.patch
BuildRequires: rubygems-devel
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildArch: noarch

%description
A gem providing "time travel" and "time freezing" capabilities, making it dead
simple to test time-dependent code.  It provides a unified method to mock
Time.now, Date.today, and DateTime.now in a single call.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T 
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -va ./%{gem_dir}/* %{buildroot}%{gem_dir}

# Fix permissions.
chmod a+x %{buildroot}%{gem_instdir}/test/run_tests.sh

%check
pushd .%{gem_instdir}/test
# Drop Bundler dependency.
sed -i '/bundler\/setup/ s/^/#/' test_helper.rb

./run_tests.sh
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.markdown
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.7.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.1-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 10 2014 Vít Ondruch <vondruch@redhat.com> - 0.7.1-1
- Update to Timecop 0.7.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Josef Stribny <jstribny@redhat.com> - 0.3.5-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.5-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Michal Fojtik <mfojtik@redhat.com> - 0.3.5-2
- Disabled test_time_stack_item test

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.3.5-1
- Initial package
