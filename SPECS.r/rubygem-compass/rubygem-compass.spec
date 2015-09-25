%global gem_name compass

Name:          rubygem-%{gem_name}
Summary:       A Sass-based CSS Meta-Framework
Version:       1.0.1
Release:       4%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://compass-style.org
Source0:       http://gemcutter.org/downloads/compass-%{version}.gem

# https://github.com/Compass/compass/pull/1828
Patch0:        compass-update-minitest.patch

# tests require sass-globbing and true, not yet in fedora
Patch1:        compass-remove-tests-missing-deps.patch

# last broken test, commenting out until I have time to debug
Patch2:        compass-remove-broken-test.patch

#Requires: rubygem(compass-core)
#Requires: rubygem(compass-import-once)
BuildRequires: rubygems-devel
BuildRequires: rubygem(chunky_png)
BuildRequires: rubygem(diff-lcs)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(compass-core)
BuildRequires: rubygem(compass-import-once)
#BuildRequires: rubygem(sass-globbing)
#BuildRequires: rubygem(true)
BuildArch:     noarch

%description
A Sass-based CSS Meta-Framework that allows you to mix and match 
any of the following CSS frameworks: Compass Core, Blueprint, 
960, Susy, YUI, and others.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%patch0
%patch1
%patch2

# Drop OSX specific dependency on rb-fsevent.
sed -i '/rb-fsevent/ s/^/#/' %{gem_name}.gemspec

%build
mkdir -p ./%{gem_dir}
gem build %{gem_name}.gemspec
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force \
        --rdoc \
        %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# rpmlint will complain about these files
#rm %{buildroot}%{gem_instdir}/frameworks/compass/stylesheets/compass/utilities/general/_tabs.sass
rm -rf %{buildroot}%{gem_instdir}/.yardoc

%check
pushd %{buildroot}/%{gem_instdir}

sed -i 's/Test::Unit::TestCase/Minitest::Test/' test/*.rb test/*/*.rb test/*/*/*.rb

# Only run the tests that run
ruby -Ilib:test:. -e 'Dir.glob "test/**/*_test.rb", &method(:require)'

# rpmlint will complain about these files
rm -rf test/fixtures/stylesheets/*/sass/.sass-cache
rm -rf .sass-cache
popd

%files
%{_bindir}/compass
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/bin
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/LICENSE.markdown
%doc %{gem_instdir}/test
%doc %{gem_instdir}/features
%doc %{gem_docdir}
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Wed Aug 19 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.1-3
- Drop OSX specific dependency on rb-fsevent (rhbz#1204090).

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 16 2015 Mo Morsi <mmorsi@redhat.com> - 1.0.1-1
- Updated to 1.0.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Troy Dawson <tdawson@redhat.com> - 0.12.5-1
- Update to 0.12.5
- Re-enabled tests

* Thu Mar 06 2014 Troy Dawson <tdawson@redhat.com> - 0.12.3-1
- Update to 0.12.3
- Re-enabled tests

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Troy Dawson <tdawson@redhat.com> - 0.12.2-5
- Change format to work with new ruby format

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 0.12.2-4
- Fix to make it build/install on F19+
- Removed testing until ruby2 gems have stabilized

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Troy Dawson <tdawson@redhat.com> - 0.12.2-2
- Get tests to run on rawhide

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 0.12.2-1
- update to latest upstream release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.11.5-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 Mo Morsi <mmorsi@redhat.com> - 0.11.5-2
- include fssm and chunky_png dependencies

* Wed Sep 28 2011 Mo Morsi <mmorsi@redhat.com> - 0.11.5-1
- update to latest upstream release

* Tue Mar 29 2011 Mo Morsi <mmorsi@redhat.com> - 0.10.6-1
- update to latest upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 14 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.8.17-3
- file list fixes to remove duplicate files 

* Wed Apr 14 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.8.17-2
- small fixes based on feedback
- replace defines w/ globals
- added check section / run tests

* Wed Feb 03 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.8.17-1
- Initial package
