%global gem_name redis-namespace

Name: rubygem-%{gem_name}
Version: 1.5.2
Release: 3%{?dist}
Summary: Namespaces Redis commands
Group: Development/Languages
License: MIT
URL: https://github.com/resque/redis-namespace
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: rubygem-redis-namespace-test.conf
# Rspec 3 support
# https://github.com/resque/redis-namespace/pull/103
Patch0: rubygem-redis-namespace-1.5.2-rspec.patch
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(redis) => 3
Requires: rubygem(redis) < 4
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec) => 3
BuildRequires: rubygem(redis) => 3
BuildRequires: rubygem(redis) < 4
BuildRequires: redis
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Adds a Redis::Namespace class which can be used to namespace calls
to Redis. This is useful when using a single instance of Redis with
multiple, different applications.


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

%patch0 -p1

# Remove dependency on bundler.
sed -i -e "/require 'bundler'/d" spec/spec_helper.rb
sed -i -e "/Bundler.setup/d" spec/spec_helper.rb
sed -i -e "/Bundler.require/d" spec/spec_helper.rb

# Remove developer-only file.
rm Rakefile
sed -i -e 's/"Rakefile",//' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
       %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  # Redis server configuration
  install -m 0644 %{SOURCE1} spec/test.conf
  mkdir spec/db

  # Start redis-server
  redis-server spec/test.conf

  # Run redis-namespace tests
  rspec -Ilib spec

  # Kill redis-server
  kill -INT `cat spec/db/redis.pid`
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
%exclude %{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.5.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 05 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.2-2
- Update to 1.5.2 (RHBZ #1207454)
- Drop Fedora 19 conditionals
- Patch for rspec 3 support
- Use %%license macro

* Thu Sep 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.1-1
- Update to 1.5.1 (RHBZ #1126616)

* Thu Jul 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-2
- Add missing gem source file

* Thu Jul 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-1
- Update to 1.5.0 (RHBZ #1114344)
- Avoid using the full path to redis-server during %%check, since this has
  changed in Fedora 21.

* Wed Jun 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.1-3
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Bump the maximum redis version.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 04 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.1-1
- Update to 1.4.1 (RHBZ #1038151)
- Use HTTPS for URL

* Thu Nov 07 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.2-2
- Update to 1.3.2

* Sat Nov 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.3.1-1
- Initial package
