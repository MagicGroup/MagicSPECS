%global gem_name creole

Name: rubygem-%{gem_name}
Version: 0.5.0
Release: 7%{?dist}
Summary: Lightweight markup language
Group: Development/Languages
# README.creole says "the same license as Ruby" and "Copyright (c) 2008", so we
# assume "GPLv2 or Ruby". It was Ruby 1.9.3 that made the transition to "Ruby
# or BSD".
License: GPLv2 or Ruby
URL: https://github.com/minad/creole
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Since we assume GPLv2 above, we'll include the full text here.
# http://www.gnu.org/licenses/gpl-2.0.txt
Source1: rubygem-creole-gpl-2.0.txt
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(bacon)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Creole is a lightweight markup language (http://wikicreole.org/).


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
for f in Gemfile Rakefile .gitignore .travis.yml; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec
rm -rf .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

install -p -m 0644 %{SOURCE1} %{buildroot}%{gem_instdir}/gpl-2.0.txt

%check
pushd .%{gem_instdir}
  bacon -q -Ilib:test test/*_test.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/gpl-2.0.txt
%doc %{gem_instdir}/README.creole
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES
%exclude %{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.5.0-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.0-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 22 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.0-3
- Correct GPLv2 license file permissions

* Tue Nov 19 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.0-2
- Update License (RHBZ #1027521)
- Change URL to use HTTPS

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.0-1
- Initial package
