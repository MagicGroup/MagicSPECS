%global gem_name resque-cleaner

Name: rubygem-%{gem_name}
Version: 0.3.0
Release: 4%{?dist}
Summary: Resque plugin to clean up failed jobs
Group: Development/Languages
License: MIT
URL: https://github.com/ono/resque-cleaner
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Update tests for Minitest 5
# Submitted upstream at https://github.com/ono/resque-cleaner/pull/32
Patch0: rubygem-resque-cleaner-0.3.0-tests.patch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(resque) => 1.0
Requires: rubygem(resque) < 2
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(timecop)
BuildRequires: rubygem(resque) => 1.0
BuildRequires: rubygem(resque) < 2
BuildRequires: rubygem(rack-test)
BuildRequires: redis
BuildRequires: procps-ng
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
resque-cleaner maintains the cleanliness of failed jobs on Resque.


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

# Remove developer-only file.
rm Rakefile
sed -i "s|\"Rakefile\",||g" %{gem_name}.gemspec

# Update tests for Minitest 5
# Submitted upstream at https://github.com/ono/resque-cleaner/pull/32
%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -Ilib test/resque_cleaner_test.rb
  ruby -Ilib test/resque_web_test.rb
popd


%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%exclude %{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 29 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.0-3
- Use %%license macro

* Sat Jul 12 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.0-2
- Add BR: procps-ng, since test suite uses "ps" to get Redis PID

* Tue May 27 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.0-1
- Update to 0.3.0
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Patch for Minitest 5

* Fri Dec 27 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.12-1
- Update to 0.2.12

* Mon Dec 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.11-1
- Initial package
