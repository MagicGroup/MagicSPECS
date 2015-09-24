%global gem_name vegas

Name: rubygem-%{gem_name}
Version: 0.1.11
Release: 3%{?dist}
Summary: Create executable versions of Sinatra/Rack apps
Group: Development/Languages
License: MIT
URL: http://code.quirkey.com/vegas/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(rack)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(bacon)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(sinatra)
BuildRequires: rubygem(thin)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Vegas aims to solve the simple problem of creating executable versions of
Sinatra/Rack apps. It includes a class Vegas::Runner that wraps Rack/Sinatra
applications and provides a simple command line interface and launching
mechanism.


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

# Remove deprecated mocha statements.
# https://github.com/quirkey/vegas/pull/20
sed -i -e "s|mocha/standalone|mocha/api|" test/test_helper.rb
sed -i -e "s|mocha/object|mocha/setup|" test/test_helper.rb

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

%check
pushd .%{gem_instdir}
  ruby -Ilib:test test/test_vegas_runner.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.rdoc
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt
%exclude %{gem_instdir}/test

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.11-1
- Initial package
