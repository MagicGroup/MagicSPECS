%global gem_name gherkin

# %%check section needs cucumber, however cucumber depends on gherkin.
%{!?need_bootstrap:	%global	need_bootstrap	0}

Summary: Fast Gherkin lexer/parser
Name: rubygem-%{gem_name}
Version: 2.11.6
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/cucumber/gherkin
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

Patch1: gherkin-2.11.6-relax-json-dependency.patch

Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(json)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
%if 0%{?need_bootstrap} < 1
BuildRequires: rubygem(cucumber)
%endif
BuildRequires: rubygem(rspec)
Provides: rubygem(%{gem_name}) = %{version}

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%description
A fast Gherkin lexer/parser based on the Ragel State Machine Compiler.


%prep
%gem_install -n %{SOURCE0}

pushd .%{gem_dir}
%patch1 -p0
popd

%build
pushd .%{gem_instdir}
pushd ext
for lexer_dir in */ ; do
    pushd $lexer_dir
    CONFIGURE_ARGS="--with-cflags='%{optflags}'" ruby extconf.rb
    make clean && make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
    make install RUBYARCHDIR="../../lib"
    popd
done

popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/lib
# the .so files go in the extdir, so remove them from lib
find %{buildroot}%{gem_instdir}/lib -iname '*.so' -exec mv {} %{buildroot}%{gem_extdir_mri}/lib \;
rm -rf %{buildroot}%{gem_instdir}/ext

# remove hidden dirs
rm -rf %{buildroot}%{gem_instdir}/features/.cucumber
rm -rf %{buildroot}%{gem_instdir}/js/.npmignore
rm -rf %{buildroot}%{gem_instdir}/js/lib/gherkin/lexer/.npmignore
find %{buildroot} -iname '.gitignore' -exec rm -f {} \;
# these files shouldn't be executable
chmod a-x %{buildroot}%{gem_instdir}/lib/gherkin/i18n.rb
chmod a-x %{buildroot}%{gem_instdir}/tasks/ragel_task.rb
chmod a-x %{buildroot}%{gem_instdir}/tasks/compile.rake

%if 0%{?need_bootstrap} < 1
%check
pushd .%{gem_instdir}
# use this gherkin, not the system one
export GEM_HOME="../../"
# kill bundler for features and specs
sed -i '7,8d' features/support/env.rb
sed -i '7,8d' spec/spec_helper.rb
# link the cucumber here for two features
ln -s %{gem_dir}/gems/cucumber-`cucumber --version`/ ../cucumber
# There is some encoding error runnign test suite with Ruby 2.0 in both,
# Cucumber and RSpec test suites:
# https://github.com/cucumber/gherkin/issues/232
# run cucumber features - 16 failed because they test fallback ruby lexers
# but these are not installed by default (even if using normal gem install)
LANG=en_US.utf8 cucumber | grep '16 failed'
# run specs, 93 fail because of the reason mentioned above
LANG=en_US.utf8 rspec spec | grep '280 examples, 93 failures'
popd
%endif

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/install_mingw_os_x.sh
%{gem_extdir_mri}
%{gem_libdir}
%{gem_instdir}/js
%{gem_instdir}/ragel
%{gem_instdir}/build_native_gems.sh
%doc %{gem_instdir}/features
%doc %{gem_instdir}/spec
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/cucumber.yml
%doc %{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/tasks

%changelog
* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 2.11.6-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Add bootstrap code.

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.11.6-1
- Updated to version 2.11.6.
- Fixed wrong dates in changelog.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 29 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.9.3-1
- Update to 2.9.3
- Introduced %%check section

* Mon Jan 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.5-4
- Removed *.so files from %%{gem_libdir}.

* Mon Jan 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.5-3
- Rebuilt for Ruby 1.9.3.
- Significantly simplified build process.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Mo Morsi <mmorsi@redhat.com> - 2.4.5-1
- Update to latest upstream release

* Wed Jun 08 2011 Chris Lalancette <clalance@redhat.com> - 2.3.3-3
- Significantly revamped spec to conform more to fedora standards
- Fix build on Rawhide

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Michal Fojtik <mfojtik@redhat.com> - 2.3.3-1
- Version bump

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 2.2.4-3
- Replaced ~> with >= in JSON version so now it can be used
  with latest json as well

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 2.2.4-2
- Fixed JSON dependency version

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 2.2.4-1
- Version bump

* Wed Sep 08 2010 Michal Fojtik <mfojtik@redhat.com> - 2.2.0-1
- Version bump

* Tue Jul 20 2010 Michal Fojtik <mfojtik@redhat.com> - 2.1.5-3
- Fixed rspec and trollop versions in gemspec files

* Tue Jul 20 2010 Michal Fojtik <mfojtik@redhat.com> - 2.1.5-2
- Added -doc subpackage
- Fixed debugging symbols issue (Thanks mtasaka)
- Fixed path for pushd in install section
- Fixed trollop version in gemspec
- Removed '#line foo' from C files

* Mon Jul 19 2010 Michal Fojtik <mfojtik@redhat.com> - 2.1.5-1
- Updated to latest version
- Fixed compiler flags
- Fixed directory ownership
- Removed unwanted versioning files
- Placed .so files on right place

* Wed Jul 14 2010 Michal Fojtik <mfojtik@redhat.com> - 2.1.3-1
- Initial package
