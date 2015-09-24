%global gem_name more_core_extensions

Name: rubygem-%{gem_name}
Version: 1.2.0
Release: 3%{?dist}
Summary: Set of core extensions beyond those provided by ActiveSupport
Group: Development/Languages
License: MIT
URL: http://github.com/ManageIQ/more_core_extensions
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(activesupport) > 3.2
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Set of core extensions beyond those provided by ActiveSupport.

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

pushd %{buildroot}%{gem_instdir}
rm .gitignore .rspec .travis.yml Gemfile Rakefile *.gemspec
popd

# Run the test suite
%check
pushd .%{gem_instdir}
#rspec -Ilib spec TODO
popd

%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/LICENSE.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 21 2014 Mo Morsi <mmorsi@redhat.com> - 1.2.0-2
- Shorten summary,
- Remove uneeded ruby BR
- Conditionalize Requires and Provides
- Use license macro

* Thu Aug 21 2014 Mo Morsi <mmorsi@redhat.com> - 1.2.0-1
- Update to latest Fedora guidelines

* Fri Aug 23 2013 Mo Morsi <mmorsi@redhat.com> - 1.1.2-1
- Release 1.1.2

* Fri Aug 23 2013 Mo Morsi <mmorsi@redhat.com> - 1.0.2-1
- Bumped version

* Fri Aug 23 2013 Mo Morsi <mmorsi@redhat.com> - 1.0.1-1
- Bumped version

* Thu Jun 20 2013 Steve Linabery <slinaber@redhat.com> - 1.0.0-1
- Initial package

