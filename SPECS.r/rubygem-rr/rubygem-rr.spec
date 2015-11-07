%global gem_name rr

%global rubyabi 1.9.1
  
%if 0%{?fedora} >= 17
  %global rubyabi 1.9.1
%endif

%if 0%{?fedora} >= 19
  %global rubyabi 2.0.0
%endif

Summary: RR (Double Ruby) is a test double framework 
Name: rubygem-%{gem_name}
Version: 1.1.2
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://pivotallabs.com
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: http://s3.amazonaws.com/rubygem-rr/tests/v%{version}.tar.gz

%if 0%{?fedora} >= 19
Requires:       ruby(release)
%endif

%if 0%{?fedora} >= 17 && 0%{?fedora} < 19
Requires:      ruby(abi) = %{rubyabi}
%endif

%if 0%{?fedora} <= 17
Requires: ruby(rubygems) 
%endif

BuildRequires: ruby-irb
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

# The following are for running test suite
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(session)
BuildRequires: rubygem(diff-lcs)
BuildRequires: rubygem(rspec)

%description
RR (Double Ruby) is a test double framework that features a rich selection of
double techniques and a terse syntax.

A Test Double is a generalization of something that replaces a real object to
make it easier to test another object. Its like a stunt double for tests.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version}

# Modify the gemspec if necessary with a patch or sed
# Also apply patches to code if necessary
# %%patch0 -p1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install

%if 0%{?fedora} >= 17 && 0%{?fedora} <= 18
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force \
        --rdoc \
        --ri \
        %{gem_name}-%{version}.gem
%endif

%if 0%{?fedora} >= 19
%gem_install
%endif

tar -xvzf %{SOURCE1}

# Run automated tests
%check
##ruby spec/suites/minitest/*_test.rb
##ruby spec/suites/test_unit/*_test.rb

# Pending failing tests
#rspec spec/suites/rspec/{*,**}/*_spec.rb
#rspec spec/suites/rspec/functional/dsl_spec.rb 
#rspec spec/suites/rspec/unit/hash_with_object_id_key_spec.rb 
#rspec spec/suites/rspec/unit/invocation_matcher_spec.rb 
#rspec spec/suites/rspec/unit/proc_from_block_spec.rb 
#rspec spec/suites/rspec/unit/rr_spec.rb 
#rspec spec/suites/rspec/unit/space_spec.rb 
#rspec spec/suites/rspec/unit/spy_verification_spec.rb 

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# Remove leftovers.
rm  %{buildroot}%{gem_instdir}/Rakefile
rm  %{buildroot}%{gem_instdir}/Appraisals
rm  -rf %{buildroot}%{gem_instdir}/gemfiles

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/CHANGES.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CREDITS.md
%exclude %{gem_cache}
%exclude %{gem_instdir}/Gemfile
%{gem_spec}
%{gem_libdir}

%files doc
%doc %{gem_docdir}/*
%{gem_instdir}/spec
%{gem_instdir}/doc
%{gem_instdir}/rr.gemspec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.2-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.2-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 18 2013 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.1.2-2
- Test suited removed temporarily
- New doc files added
- CREDITS.md file added

* Sun Aug 18 2013 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.1.2-1
- Updated version 1.1.2

* Thu Aug 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.5-3
- Don't kill VERSION file to make rr really work (bug 993490)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 21 2013 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.0.5-1
- Updated version 1.0.5
- Automated tests included 
- rubygem(rspec) included as a build require

* Sun Mar 24 2013 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.0.4-7
- Removed unnecesary dependencies
- Fixes for Ruby 2.0.0 packaging

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.4-8
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.0.4-6
- Removed unnecesary dependencies
- Spec adjusted according new guidelines

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 12 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.0.4-4
- Changelog entries fixed

* Tue Feb 07 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.0.4-3
- Updated spec file for Ruby 1.9 guidelines
- RSPec 1x tests disabled

* Tue Jan 24 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.0.4-2
- Removed unused macro from spec file
- Removed doc tag for benchmarks and spec file
- Removed cached version of the gem
- Fixed test suite files and test suite enabled at check section

* Sat Jan 21 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.0.4-1
- Initial package
