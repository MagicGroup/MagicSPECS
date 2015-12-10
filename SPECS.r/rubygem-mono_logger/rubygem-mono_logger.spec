%global gem_name mono_logger

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 6%{?dist}
Summary: A lock-free logger compatible with Ruby 2.0
Group: Development/Languages
License: MIT
URL: https://github.com/steveklabnik/mono_logger
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Minitest 5 support
# https://github.com/steveklabnik/mono_logger/pull/3
Patch0: rubygem-mono_logger-1.1.0-minitest.patch
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A lock-free logger compatible with Ruby 2.0. Ruby does not allow you to
request a lock in a trap handler because that could deadlock, so Logger is not
sufficient.


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

# Minitest 5 support
%patch0 -p1

# Remove developer-only files.
for f in Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -Ilib test/*_test.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.1.0-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-4
- 为 Magic 3.0 重建

* Fri Jul 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-3
- Patch for Minitest 5 support (RHBZ #1107169)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-1
- Initial package
