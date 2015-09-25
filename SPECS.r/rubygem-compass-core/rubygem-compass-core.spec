# Generated from compass-core-1.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name compass-core

Name: rubygem-%{gem_name}
Version: 1.0.1
Release: 6%{?dist}
Summary: The Compass core stylesheet library
Group: Development/Languages
License: MIT
URL: http://compass-style.org/reference/compass/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# upstream gem doesn't ship tests, pull in from upstream
# git clone https://github.com/compass/compass.git
# cd compass
# git checkout 1.0.1
# tar czvf rubygem-compass-core-tests.tgz core/test
Source1: rubygem-compass-core-tests.tgz

# http://github.com/compass/compass/issue/1828
# backported to compass 1.0.1
Patch0: minitest5-core-1.0.1.patch

BuildRequires: rubygems-devel 
BuildRequires: rubygem(minitest) >= 5
BuildRequires: rubygem(diff-lcs)
BuildRequires: rubygem(sass)
BuildRequires: rubygem(multi_json)
BuildRequires: rubygem(timecop)
#BuildRequires: rubygem(true)
BuildArch: noarch

%description
The Compass core stylesheet library and minimum required ruby extensions. This
library can be used stand-alone without the compass ruby configuration file or
compass command line tools.


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

tar xzvf %{SOURCE1}

patch -p1 < %{PATCH0}

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

mv core/test .%{gem_instdir}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Run the test suite
%check
pushd .%{gem_instdir}
ruby -Ilib:test/units \
     -e 'Dir.glob "./test/units/*_test.rb", &method(:require)'

# this test will be fixed in next release:
# http://github.com/Compass/compass/commit/fc349ef9f2ad18fc0456e6c19510a47d3d6830c9
#ruby -Ilib:test/integrations test/integrations/projects_test.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt
%{gem_instdir}/data/
%{gem_instdir}/stylesheets
%{gem_instdir}/templates
%exclude %{gem_instdir}/test

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.1-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 23 2014 Mo Morsi <mmorsi@redhat.com> - 1.0.1-4
- Exclude tests from files
- Change test invocation command

* Tue Sep 16 2014 Mo Morsi <mmorsi@redhat.com> - 1.0.1-3
- Run tests, add BRs to do so

* Thu Aug 28 2014 Mo Morsi <mmorsi@redhat.com> - 1.0.1-2
- Remove uneeded Requires

* Tue Aug 19 2014 Mo Morsi <mmorsi@redhat.com> - 1.0.1-1
- Initial package
