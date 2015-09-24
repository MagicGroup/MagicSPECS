%global gem_name pathspec

Name:           rubygem-%{gem_name}
Version:        0.0.2
Release:        3%{?dist}
Summary:        Use to match path patterns such as gitignore

License:        ASL 2.0
URL:            https://rubygems.org/gems/%{gem_name}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
# svn export https://github.com/highb/pathspec-ruby/tags/0.0.2/spec spec
# tar caf spec-0.0.2.tar.xz spec
Source1:        spec-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  rubygems-devel
BuildRequires:  rubygem(rspec)
BuildRequires:  rubygem(fakefs)

%description
Use to match path patterns such as gitignore.


%package doc
Summary:        Documentation for %{name}
Requires:       rubygems

%description doc
Documentaion for %{name}


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version} -a 1
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%if 0%{fedora} < 22
  # Fedora 21 has Rspec 2.x, and Fedora 22 has Rspec 3.x.
  # Switch to the older Rspec functions.
  for f in $(find spec -type f); do
    sed -i $f \
      -e "s/is_expected\.to/should/g" \
      -e "s/is_expected\.not_to/should_not/g"
  done
%endif


%build
gem build %{gem_name}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
rspec -Ilib spec


%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Orion Poplawski <orion@cora.nwra.com> - 0.0.2-2
- Fix files
- Doc subpackage
- Run tests

* Fri Apr 10 2015 Orion Poplawski <orion@cora.nwra.com> - 0.0.2-1
- Initial package
