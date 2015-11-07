%global gem_name occi-cli

Name:           rubygem-%{gem_name}
Version:        4.3.1
Release:        4%{?dist}
Summary:        Executable OCCI client

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/EGI-FCTF/rOCCI-cli
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/EGI-FCTF/rOCCI-cli/pull/14
Source1:        occi.1

BuildArch:      noarch
# occi-cli should work with jruby, but there are some problems in Fedora
BuildRequires:  ruby
BuildRequires:  ruby(release) >= 1.9.3
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(json)
BuildRequires:  rubygem(occi-api) => 4.3.1
BuildRequires:  rubygem(occi-api) < 4.4
BuildRequires:  rubygem(rspec)

%description
This gem is a client implementation of the Open Cloud Computing Interface in
Ruby.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# relax dependencies
sed -i -e 's|\(%q<json>,\) \[.*\]|\1 [">= 1.7.7"]|' %{gem_name}.gemspec

# standard shebang
sed -i '1{s,^#.*,#!/usr/bin/ruby,}' bin/occi


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/


%check
pushd .%{gem_instdir}
rspec -Ilib spec
popd


%files
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/README.md
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}/
%{_bindir}/occi
%{_mandir}/man1/occi.1*
%{gem_instdir}/bin/
%{gem_libdir}/
%{gem_spec}
%exclude %{gem_cache}
%exclude %{gem_instdir}/spec/
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.rspec
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.yardopts
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/config/warble.rb

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/doc/macosx.md


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 4.3.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.3.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 František Dvořák <valtri@civ.zcu.cz> - 4.3.1-1
- Initial package
