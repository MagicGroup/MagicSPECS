# Generated from web-console-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name web-console

Name: rubygem-%{gem_name}
Version: 2.1.3
Release: 3%{?dist}
Summary: A debugging tool for your Ruby on Rails applications
Group: Development/Languages
License: MIT
URL: https://github.com/rails/web-console
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(binding_of_caller)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(sqlite3)
BuildArch: noarch

%description
A debugging tool for your Ruby on Rails applications.


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

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


# Run the test suite
%check
pushd .%{gem_instdir}
# We don't care about code coverage.
sed -i '/imple.ov/ s/^/#/' test/test_helper.rb

# Couldn't find a way how to execute the test suite without Bundler,
# so give it some reasonable Gemfile.
cat << \EOF > Gemfile
source 'https://rubygems.org'

gem 'binding_of_caller'
gem 'mocha', require: false
gem 'rails'
gem 'sqlite3'
EOF

ruby -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%license %{gem_instdir}/MIT-LICENSE
%dir %{gem_instdir}
# This contains generated RoR app with various stuff, better to ommit it.
%exclude %{gem_instdir}/test
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.1.3-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.3-2
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Vít Ondruch <vondruch@redhat.com> - 2.1.3-1
- Update to web-console 2.1.3.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Vít Ondruch <vondruch@redhat.com> - 2.0.0-1
- Initial package
