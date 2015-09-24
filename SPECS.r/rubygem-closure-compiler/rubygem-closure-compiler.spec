# Generated from closure-compiler-1.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name closure-compiler

Name: rubygem-%{gem_name}
Version: 1.1.11
Release: 1%{?dist}
Summary: Ruby Wrapper for the Google Closure Compiler
Group: Development/Languages
License: ASL 2.0
URL: http://github.com/documentcloud/closure-compiler/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/documentcloud/closure-compiler.git && cd closure-compiler
# git checkout 1.1.11 && tar czvf closure-compiler-1.1.11-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
# Fix test compatibility with Fedoras Closure Compiler.
Patch0: rubygem-closure-compiler-1.1.11-Closure-Compiler-20141215-compatibility.patch
BuildRequires: %{_bindir}/closure-compiler
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(test-unit)
BuildRequires: %{_bindir}/closure-compiler
BuildArch: noarch

%description
A Ruby Wrapper for the Google Closure Compiler.


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

# Remove bundled closure-compiler.
rm lib/*.jar
sed -i 's| "lib/closure-compiler-20140730.jar",||' %{gem_name}.gemspec

# Update the loader with proper paths. Hopefully, the disabled constants does
# not make any troubles to our users.
sed -i '/^  COMPILER_VERSION/ s/^/#/' lib/closure-compiler.rb
sed -i '/^  COMPILER_ROOT/ s/^/#/' lib/closure-compiler.rb
sed -i 's|File.join(COMPILER_ROOT, "closure-compiler-#{COMPILER_VERSION}.jar")|File.join("%{_javadir}/%{gem_name}", "closure-compiler.jar")|' lib/closure-compiler.rb

# Use the closure-compiler wrapper script.
# https://fedoraproject.org/wiki/Packaging:Java#Wrapper_Scripts
# Unfortunately, this breaks the possibility to pick different Closure
# Compiler version. Not sure how widely this feature is used. Lets see.
sed -i 's|@java, '"'"'-jar'"'"', "\\"#{@jar}\\""|"closure-compiler"|' lib/closure/compiler.rb


%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

cat %{PATCH0} | patch -p1

# The .jar was unbundled, so no need to check its permissions.
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)' - \
  --ignore-name=/test_permissions/

popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/COPYING
%license %{gem_instdir}/LICENSE
# This is not the original file, so rather drop it.
%exclude %{gem_instdir}/closure-compiler.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.textile

%changelog
* Mon Aug 24 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.11-1
- Update to closure-compiler 1.1.11.

* Tue Jul 26 2011 Vít Ondruch <vondruch@redhat.com> - 1.1.1-1
- Initial package
