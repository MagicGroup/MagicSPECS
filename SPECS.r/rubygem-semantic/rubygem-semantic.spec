%global gem_name semantic

Name:           rubygem-%{gem_name}
Version:        1.4.1
Release:        3%{?dist}
Summary:        Utility class for parsing, storing, and comparing versions

License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildArch:      noarch

BuildRequires:  rubygems-devel
BuildRequires:  rubygem(rspec)

%description
Semantic Version utility class for parsing, storing, and comparing versions.


%package doc
Summary:        Documentation for %{name}
Requires:       rubygems

%description doc
Documentation for %{name}


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
rm -r %{buildroot}%{gem_instdir}/spec


%check
rspec -Ilib spec


%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Orion Poplawski <orion@cora.nwra.com> - 1.4.1-1
- Update to 1.4.1

* Sat Apr 18 2015 Orion Poplawski <orion@cora.nwra.com> - 1.4.0-3
- Fix typo
- Make doc require rubygems
- Mark doc %%{doc}
- Use %%{gem_libdir}

* Sun Apr 12 2015 Orion Poplawski <orion@cora.nwra.com> - 1.4.0-2
- Fix license
- Add BR rubygem(rspec)

* Fri Apr 10 2015 Orion Poplawski <orion@cora.nwra.com> - 1.4.0-1
- Initial package
