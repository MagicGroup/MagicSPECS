# Generated from tzinfo-0.3.26.gem by gem2rpm -*- rpm-spec -*-
%global gem_name tzinfo

%global download_path http://rubygems.org/downloads/

Summary: Daylight-savings aware timezone library
Name: rubygem-%{gem_name}
Version: 1.2.2
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://tzinfo.github.io/
Source0: %{download_path}%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: rubygem(thread_safe)
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
TZInfo is a Ruby library that uses the standard tz (Olson) database to provide
daylight savings aware transformations between times in different time zones.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ruby -Ilib -e "require './test/ts_all'"
ruby -Ilib -e "require './test/ts_all_zoneinfo.rb'"
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.yardopts
%{gem_spec}

%files doc
%doc %{gem_instdir}/CHANGES.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/%{gem_name}.gemspec
%{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.2-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 1.2.2-1
- Update to 1.2.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Josef Stribny <jstribny@redhat.com> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Patch tzinfo to use Minitest 5

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 1.1.0-1
- Update to tzinfo 1.1.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Josef Stribny <jstribny@redhat.com> - 0.3.37-1
- Update to tzinfo 0.3.37.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.35-1
- Update to tzinfo 0.3.35.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.34-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.34-1
- Update to tzinfo 0.3.34.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.30-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 06 2011 Vít Ondruch <vondruch@redhat.com> - 0.3.30-1
- Update to tzinfo 0.3.30.

* Sun Apr 10 2011  <Minnikhanov@gmail.com> - 0.3.26-1
- Updated mail to latest upstream release (v.0.3.26 2011-04-01)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011  <Minnikhanov@gmail.com> - 0.3.24-2
- Fix Comment 3 #668098. https://bugzilla.redhat.com/show_bug.cgi?id=668098#c3 

* Tue Jan 18 2011  <Minnikhanov@gmail.com> - 0.3.24-1
- Updated mail to latest upstream release

* Sat Jan 08 2011  <Minnikhanov@gmail.com> - 0.3.23-1
- Initial package

