%global gem_name geoip

Name: rubygem-%{gem_name}
Version: 1.5.0
Release: 4%{?dist}
Summary: Search a GeoIP database for an IP address
Group: Development/Languages
License: LGPLv2+
URL: https://github.com/cjheath/geoip
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

# The ruby(release) package already provides a usable Ruby interpreter.
# Filter the extra /usr/bin/ruby requirement here.
%global __requires_exclude ^/usr/bin/ruby$

%description
GeoIP searches a GeoIP database for a given host or IP address, and
returns information about the country where the IP address is allocated,
and the city, ISP and other information, if you have that database version.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Fix shebang
sed -i -e 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' bin/%{gem_name}

# Clean up development-only file
rm Rakefile
sed -i "s|\"Rakefile\",||g" %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
  ruby -I"lib:." test/test_geoip.rb
popd

%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.rdoc
%{_bindir}/%{gem_name}
%{gem_instdir}/bin
%{gem_instdir}/data
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.rdoc
%exclude %{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.5.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.5.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-1
- Update to 1.5.0 (RHBZ #1201073)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Use %%license macro
- Remove macro in %%changelog to satisfy rpmlint

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.0-2
- Add Minitest 5 support

* Wed Apr 02 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.0-1
- Update to 1.4.0 (RHBZ #1080916)

* Sat Dec 28 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.5-1
- Update to 1.3.5
- Remove obsolete comments
- Remove Rakefile during %%prep
- Move README to the main package
- Exclude tests from the binary packages

* Thu Oct 24 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.3-1
- Update to 1.3.3

* Mon Oct 07 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.2-1
- Update to 1.3.2
- Drop our LGPL license file, since upstream ships their own

* Fri Sep 13 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.0-2
- Fix issues in package review (RHBZ #993482). Thanks jvcelak
- Fix LICENSE file permissions
- Simplify Requires and BuildRequires

* Thu Sep 12 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.0-1
- Update to 1.3.0
- Include LGPLv2+ license text

* Mon Aug 05 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.2.2-1
- Initial package
