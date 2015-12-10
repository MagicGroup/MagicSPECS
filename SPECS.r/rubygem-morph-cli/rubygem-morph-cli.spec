%global commit cfb3b14c0e8e9e2dee48346d53c4fce8d1196d8d
%global gem_name morph-cli

Name:           rubygem-%{gem_name}
Version:        0.2.2
Release:        6%{?dist}
Summary:        Runs Morph scrapers from the command line

Group:          Development/Tools
License:        MIT
URL:            https://github.com/openaustralia/morph-cli
Source0:        https://github.com/openaustralia/%{gem_name}/archive/%{commit}/%{gem_name}-%{commit}.tar.gz
Patch0:         0001-Disallow-gzip.patch
BuildArch:      noarch

BuildRequires:  rubygems-devel
BuildRequires:  rubygem(json_pure)
BuildRequires:  git
Requires:       ruby(release) >= 1.9
Requires:       rubygem(thor) >= 0.17
Requires:       rubygem(rest-client)
Requires:       rubygem(archive-tar-minitar)
Requires:       rubygems

%description
Actually it will run them on the Morph server identically to the real thing.
That means not installing a bucket load of libraries and bits and bobs that are
already installed with the Morph scraper environments.


%prep
%setup -qn %{gem_name}-%{commit}
%patch0 -p1

# Someone had a clever idea to use "git ls-files" to obtain the list of
# sources. Oh well, let's just pretend we're an actual Git checkout.
git init
git config user.name 'Fedora package maintainers'
git config user.email '%{name}-owner@fedoraproject.org'
git add lib
git commit -m 'Import'


%build
gem build %{gem_name}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_bindir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}


%files
%{_bindir}/*
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_docdir}
%{gem_spec}
%doc LICENSE.txt README.md scraper.rb


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.2.2-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.2-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.2-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Lubomir Rintel <lkundrak@v3.sk> - 0.2.2-1
- New upstream release

* Sat Jul 12 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.2.1-2
- Disallow gzip TE

* Sun Jun  8 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.2.1-1
- New upstream release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.2-1
- Initial packaging
