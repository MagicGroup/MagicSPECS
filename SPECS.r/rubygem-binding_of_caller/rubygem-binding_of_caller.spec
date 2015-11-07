# Generated from binding_of_caller-0.7.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name binding_of_caller

Name: rubygem-%{gem_name}
Version: 0.7.2
Release: 4%{?dist}
Summary: Retrieve the binding of a method's caller
Group: Development/Languages
License: MIT
URL: http://github.com/banister/binding_of_caller
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby-devel 
BuildRequires: rubygem(bacon) 
BuildRequires: rubygem(debug_inspector) 
BuildArch: noarch

%description
Retrieve the binding of a method's caller. Can also retrieve bindings even
further up the stack.


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

# The extension is not needed for Ruby 2.0.0+, so drop it entirely.
sed -i '/s\.extensions/ d' %{gem_name}.gemspec
sed -i 's|, "ext/[^"]*"||g' %{gem_name}.gemspec

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

# Fix executable bits.
# https://github.com/banister/binding_of_caller/commit/9337eb11f71e45b156b2a7567aca05cbc93acf80
find %{buildroot}%{gem_instdir} -type f -perm /a+x | xargs chmod a-x

# Run the test suite
%check
pushd .%{gem_instdir}
bacon -a
popd

%files
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/HISTORY
%{gem_instdir}/Rakefile
# This is not the upstream .gemspec anyway.
%exclude %{gem_instdir}/binding_of_caller.gemspec
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.7.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.2-1
- Initial package
