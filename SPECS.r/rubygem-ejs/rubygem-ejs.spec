# Generated from ejs-1.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ejs

Name: rubygem-%{gem_name}
Version: 1.1.1
Release: 3%{?dist}
Summary: EJS (Embedded JavaScript) template compiler
Group: Development/Languages
License: MIT
URL: https://github.com/sstephenson/ruby-ejs/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/sstephenson/ruby-ejs/ && cd ruby-ejs/
# git checkout v1.1.1 && tar czf ejs-1.1.1-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(execjs)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(therubyracer)
BuildArch: noarch

%description
Compile and evaluate EJS (Embedded JavaScript) templates from Ruby.


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
tar xzf %{SOURCE1}

ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.1-1
- Initial package
