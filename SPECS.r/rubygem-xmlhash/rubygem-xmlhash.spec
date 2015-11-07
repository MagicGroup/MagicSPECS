%global gem_name xmlhash

Name: rubygem-%{gem_name}
Version: 1.3.6
Release: 8%{?dist}
Summary: A small C module to parse a XML string into a ruby hash
Group: Development/Languages
License: MIT
URL: https://github.com/coolo/xmlhash
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: libxml2
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby-devel 
BuildRequires: libxml2 libxml2-devel
BuildRequires: rubygem(pkg-config)
#tests
BuildRequires: rubygem(json)
BuildRequires: rubygem(minitest)

%description
A small C module that wraps libxml2's xmlreader to parse a XML
string into a ruby hash.


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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/xmlhash
cp -a ./%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/
cp -a ./%{gem_extdir_mri}/xmlhash/*.so %{buildroot}%{gem_extdir_mri}/xmlhash/

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext
rm -f %{buildroot}%{gem_instdir}/{.gemtest,.autotest,.travis.yml}

%check
pushd .%{gem_instdir}
# Minitest 5
# https://github.com/coolo/xmlhash/pull/3
sed -i "s|test/unit|minitest/autorun|" ./test/test_xmlhash.rb
sed -i "s/Test::Unit::TestCase/Minitest::Test/" ./test/test_xmlhash.rb
ruby -Ilib -I$(dirs +1)%{gem_extdir_mri} -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.3.6-8
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.6-7
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 1.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Josef Stribny <jstribny@redhat.com> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Thu Sep 12 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.6-1
- rebase to 1.3.6

* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-5
- 988818 - actually run the test suite
- 988818 - move README.txt to main package
- 988818 - summary-too-long
- 988818 - escape macro in comment

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-4
- BR minitest

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-3
- run test
- fix files section
- Remove the binary extension sources and build leftovers.
- add BuildRequires rubygem(pkg-config)
- require libxml2 and BR libxml2, libxml2-devel

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-2
- initial package

