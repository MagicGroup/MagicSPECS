%global gem_name mizuho
# Although there are tests, they don't work yet
# https://github.com/FooBarWidget/mizuho/issues/5
%global enable_tests 0

Summary:       Mizuho documentation formatting tool
Name:          rubygem-%{gem_name}
Version:       0.9.20
Release:       5%{?dist}
Group:         Development/Languages
License:       MIT
URL:           https://github.com/FooBarWidget/mizuho
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch1:        rubygem-mizuho-0.9.20-fix_native_templates_dir.patch
Requires:      asciidoc
Requires:      ruby(release)
Requires:      ruby(rubygems) 
Requires:      rubygem(nokogiri) >= 1.4.0
Requires:      rubygem(sqlite3) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
%if 0%{?enable_tests}
BuildRequires: rubygem-rspec
%endif
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
A documentation formatting tool. Mizuho converts Asciidoc input files into
nicely outputted HTML, possibly one file per chapter. Multiple templates are
supported, so you can write your own.


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

# Unbundle asciidoc
rm -rf asciidoc
sed -i 's/NATIVELY_PACKAGED = .*/NATIVELY_PACKAGED = true/' lib/mizuho.rb
sed -i -e 's\ "asciidoc[^,]*,\\g' %{gem_name}.gemspec

# Fixup rpmlint failures
echo "#toc.html" >> templates/toc.html

%patch1 -p 1

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Remove build leftovers.
rm -rf %{buildroot}%{gem_instdir}/{.rvmrc,.document,.require_paths,.gitignore,.travis.yml,.rspec,.gemtest,.yard*}
rm -rf %{buildroot}%{gem_instdir}/%{gem_name}.gemspec

%if 0%{?enable_tests}
%check
pushd %{buildroot}%{gem_instdir}
ruby -Ilib -S rspec -f s -c test/*_spec.rb
popd
%endif

%files
%doc %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%{_bindir}/mizuho
%{_bindir}/mizuho-asciidoc
%{gem_instdir}/bin
%{gem_instdir}/debian.template
%{gem_instdir}/rpm
%{gem_instdir}/source-highlight
%{gem_instdir}/templates
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.markdown
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/test


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Troy Dawson <tdawson@redhat.com> - 0.9.20-3
- Fix native templated directory (#1072246)

* Wed Feb 19 2014 Troy Dawson <tdawson@redhat.com> - 0.9.20-2
- Remove bundled asciidoc

* Thu Feb 06 2014 Troy Dawson <tdawson@redhat.com> - 0.9.20-1
- Initial package
