# Generated from fog-xml-0.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-xml

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 4%{?dist}
Summary: XML parsing for fog providers
Group: Development/Languages
License: MIT
URL: https://github.com/fog/fog-xml
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(fog-core)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
BuildArch: noarch

%description
Extraction of the XML parsing tools shared between a
number of providers in the 'fog' gem.


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

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
# We don't have Turn in Fedora (neither we really need it).
sed -i '/require.*turn/ s/^/#/' spec/minitest_helper.rb
sed -i '/Turn/,/end/ s/^/#/' spec/minitest_helper.rb

ruby -Ilib:spec -e 'Dir.glob "./spec/**/*_spec.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE.md
%exclude %{gem_instdir}/fog-xml.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/CONTRIBUTORS.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles
%{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.1.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Vít Ondruch <vondruch@redhat.com> - 0.1.1-1
- Initial package
