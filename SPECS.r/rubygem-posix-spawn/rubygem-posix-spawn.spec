%global gem_name posix-spawn

Name: rubygem-%{gem_name}
Version: 0.3.9
Release: 2%{?dist}
Summary: posix_spawnp(2) for Ruby
Group: Development/Languages
License: MIT and LGPLv2+
URL: https://github.com/rtomayko/posix-spawn
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} && 0%{?fedora} < 21
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
%endif
# Skip tests that fail.
# https://github.com/rtomayko/posix-spawn/issues/43
Patch0: rubygem-posix-spawn-0.3.9-skip-tests.patch
# Minitest 5 support
# https://github.com/rtomayko/posix-spawn/pull/65
Patch1: rubygem-posix-spawn-0.3.9-minitest.patch
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(minitest)
%if 0%{?fedora} && 0%{?fedora} < 21
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
posix-spawn uses posix_spawnp(2) for faster process spawning


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
for f in .gitignore Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Skip tests that fail.
# https://github.com/rtomayko/posix-spawn/issues/43
%patch0 -p1
# Minitest 5 support
%patch1 -p1
# Patch1 creates a new test/test_helper.rb file, but we have to add this file
# to the files list using sed, rather than the more exact method of doing this
# inside Patch1. The reason is that Fedora's packaging generates
# posix-spawn.gemspec dynamically during each RPM build (see the "gem spec"
# line above), so the gemspec file from the RPM can look slightly different
# each time, and a static patch may or may not apply cleanly.
sed -i posix-spawn.gemspec -e '/s.files/s/]/, "test\/test_helper.rb"]/'

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec file
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove deprecated "ext" directory
rm -r %{buildroot}%{gem_instdir}/ext

# Move the binary extension.
# Get the minor version number of Ruby
ruby_version_minor=$(ruby \
  -e "puts RUBY_VERSION.split('.')[1]")
# Move according to Ruby 2.1 or 2.0
if [ $ruby_version_minor -gt 0 ]; then
  # Ruby 2.1+ on Fedora 21 and above
  mkdir -p %{buildroot}%{gem_extdir_mri}
  cp -pa .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/
else
  # Ruby 2.0 on Fedora 20
  mkdir -p %{buildroot}%{gem_extdir_mri}/lib
  mv %{buildroot}%{gem_libdir}/posix_spawn_ext.so \
    %{buildroot}%{gem_extdir_mri}/lib/
fi

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
  ruby -I"lib:test:%{buildroot}%{gem_extdir_mri}" -e \
    'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/README.md
%{_bindir}/posix-spawn-benchmark
%{gem_instdir}/bin
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/HACKING
%doc %{gem_instdir}/TODO
%exclude %{gem_instdir}/test

%changelog
* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Thu Sep 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.9-1
- Update to 0.3.9 (RHBZ #1125902)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
  and Minitest 5

* Fri Dec 27 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.8-1
- Initial package
