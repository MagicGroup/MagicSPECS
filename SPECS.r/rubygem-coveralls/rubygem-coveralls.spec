%global gem_name coveralls

Summary:       A Ruby implementation of the Coveralls API
Name:          rubygem-%{gem_name}
Version:       0.8.2
Release:       4%{?dist}
Group:         Development/Languages
License:       MIT
URL:           https://coveralls.io
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires:      ruby(release)
Requires:      ruby(rubygems)
Requires:      rubygem(multi_json)
Requires:      rubygem(rest-client)
Requires:      rubygem(simplecov)
Requires:      rubygem(term-ansicolor)
Requires:      rubygem(thor)
%endif
BuildRequires: git
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(multi_json)
BuildRequires: rubygem(rake)
BuildRequires: rubygem(rest-client)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(simplecov)
BuildRequires: rubygem(term-ansicolor)
BuildRequires: rubygem(thor)
BuildRequires: rubygem(vcr)
BuildRequires: rubygem(webmock)
BuildRequires: txt2man
BuildArch:     noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7} || 0%{?el6}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Coveralls works with your continuous integration 
server to give you test coverage history and statistics.

This package is a Ruby implementation of the Coveralls API.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

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

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

chmod 755 %{buildroot}%{gem_instdir}/Rakefile
find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
find %{buildroot}%{gem_instdir}/spec -name *.rb | xargs chmod a-x

# Create man pages
mkdir -p %{buildroot}%{_mandir}/man1
%{buildroot}%{gem_instdir}/bin/coveralls help > helpfile
txt2man -P coveralls -t coveralls -r %{version} helpfile > %{buildroot}%{_mandir}/man1/coveralls.1
rm -f helpfile

# Remove build leftovers.
rm -rf %{buildroot}%{gem_instdir}/{.gitignore,.rspec,.ruby-version,.travis.yml,.yard*}
rm -f %{buildroot}%{gem_instdir}/{Gemfile,coveralls-ruby.gemspec}

%check
pushd ./%{gem_instdir}
rspec -Ilib spec
popd

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{_bindir}/coveralls
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{_mandir}/man1/*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.8.2-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.8.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.2-2
- 为 Magic 3.0 重建

* Mon Jul 27 2015 Troy Dawson <tdawson@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jul 18 2014 Troy Dawson <tdawson@redhat.com> - 0.7.0-4
- Spec file tweaks to accomodate different releases (#1121107)

* Mon Jul 07 2014 Troy Dawson <tdawson@redhat.com> - 0.7.0-3
- Spec file tweaks

* Thu Jul 03 2014 Troy Dawson <tdawson@redhat.com> - 0.7.0-2
- Add man page

* Wed Apr 02 2014 Troy Dawson <tdawson@redhat.com> - 0.7.0-1
- Initial package
