%global gem_name loofah

Name: rubygem-%{gem_name}
Version: 2.0.2
Release: 4%{?dist}
Summary: Manipulate and transform HTML/XML documents and fragments
Group: Development/Languages
License: MIT
URL: https://github.com/flavorjones/loofah
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(nokogiri) >= 1.6.6.2
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(nokogiri) >= 1.6.6.2
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rr)
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Loofah is a general library for manipulating and transforming HTML/XML
documents and fragments. It's built on top of Nokogiri and libxml2, so
it's fast and has a nice API.
Loofah excels at HTML sanitization (XSS prevention). It includes some
nice HTML sanitizers, which are based on HTML5lib's whitelist, so it
most likely won't make your codes less secure.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Remove developer-only files.
for f in .gemtest Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",*||g" %{gem_name}.gemspec
done

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a  .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -I"lib:test" -e \
    'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd


%files
%dir %{gem_instdir}
%{!?_licensedir:%global license %%doc}
%license %{gem_instdir}/MIT-LICENSE.txt
%doc %{gem_instdir}/README.rdoc
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/CHANGELOG.rdoc
%exclude %{gem_instdir}/benchmark
%exclude %{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.0.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.0.2-1
- Update to loofah 2.0.2 (rhbz#1218819)
- Drop patch to skip failing test (it works now, with Nokogiri 1.6.6.2)
- Drop Fedora 19 support
- Use %%license macro

* Thu Sep 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.0.1-1
- Update to loofah 2.0.1 (RHBZ #1132898)
- Drop upstreamed RR patch

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.0.0-1
- Update to loofah 2.0.0 (RHBZ #1096760)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sat Dec 28 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.2.1-1
- Initial package
