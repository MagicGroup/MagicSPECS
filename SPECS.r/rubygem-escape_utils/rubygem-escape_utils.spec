%global gem_name escape_utils

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 5%{?dist}
Summary: Faster string escaping routines for your web apps
Group: Development/Languages
License: MIT
URL: https://github.com/brianmario/escape_utils
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Quickly perform HTML, URL, URI and Javascript escaping/unescaping.


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

# Remove developer-only files.
for f in .gitignore .travis.yml Gemfile Rakefile benchmark/* script/*; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Remove dependency on bundler
sed -e "/require 'bundler\/setup'/d" -i test/helper.rb

# Get the major version number of the Minitest gem
minitest=$(ruby -r 'minitest/unit' \
  -e "puts Minitest::Unit::VERSION.split('.')[0]")
if [ $minitest < 5 ]; then
  # Conditionally correct Minitest usage, for Minitest versions < 5.0.0.
  # For example, at least Fedora 20 has Minitest 4.x.
  for f in $(find test -type f); do
    sed -i "s/Minitest::Test/Minitest::Unit::TestCase/g" $f
  done
fi

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec file
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Move the binary extension
%if 0%{?fc20} || 0%{?el7}
  mkdir -p %{buildroot}%{gem_extdir_mri}/lib/%{gem_name}
  mv %{buildroot}%{gem_libdir}/%{gem_name}/%{gem_name}.so \
    %{buildroot}%{gem_extdir_mri}/lib/%{gem_name}
%else
  mkdir -p %{buildroot}%{gem_extdir_mri}
  cp -a .%{gem_extdir_mri}/{gem.build_complete,%{gem_name}} \
    %{buildroot}%{gem_extdir_mri}/
%endif

# Remove deprecated "ext" directory, preventing dangling symlink in -debuginfo
# (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext


%check
pushd .%{gem_instdir}
  ruby -I"lib:%{buildroot}%{gem_extdir_mri}" -e \
  'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd


%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.1.0-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-1
- Update to escape_utils 1.1.0
- Drop Fedora 19 support
- Simplify "bench" and "scripts" directory removals in %%prep
- Fix comparison for Minitest::Unit::TestCase backwards compatibility
- Use %%license macro

* Thu Jan 15 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-3
- Use %%{gem_name} during binary extension installation (RHBZ #1046995)

* Thu May 08 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-2
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Update %%check for Minitest 5

* Sat Feb 15 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-1
- Update to escape_utils 1.0.1
- Remove benchmark directory during %%prep

* Sat Dec 28 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.0-2
- Ship escape_utils.so in the correct location

* Fri Dec 27 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.0-1
- Initial package
