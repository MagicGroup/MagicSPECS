%global gem_name org-ruby

Name: rubygem-%{gem_name}
Version: 0.9.12
Release: 2%{?dist}
Summary: Ruby routines for parsing org-mode files
Group: Development/Languages
License: MIT
URL: https://github.com/wallyqs/org-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Upstream does not ship the test suite in the gem.
Source1: %{name}-generate-test-tarball.sh
Source2: %{gem_name}-%{version}-tests.tar.xz
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(rubypants)
Requires: rubygem(tilt)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rubypants)
BuildRequires: rubygem(tilt)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
An org-mode parser written in Ruby. This gem contains Ruby routines for
parsing org-mode files. The most significant thing this library does
today is convert org-mode files to HTML or textile. Currently, you
cannot do much to customize the conversion. The supplied textile
conversion is optimized for extracting "content" from the orgfile as
opposed to "metadata."


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version} -a 2

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Conditionally correct RSpec usage for RSpec version 2.
# Fedora 21 has RSpec 2, and Fedora 22 will have RSpec 3.
# Get the major version number of the Rspec gem
rspec=$(ruby -r 'rspec/core' \
  -e "puts RSpec::Core::Version::STRING.split('.')[0]")
if [ $rspec == 2 ]; then
  # Switch to the older Rspec function.
  for f in $(find spec -type f); do
    sed -i -e "s/be_truthy/be_true/g" -e "s/be_falsy/be_false/g" $f
  done
fi

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
export LANG=en_US.UTF-8
cp -pr spec .%{gem_instdir}
pushd .%{gem_instdir}
  # Note: the tests may fail because the HTML output has historically been
  # tightly coupled with specific Tilt versions.
  # You can check upstream's Travis CI status for more information or help.
  # https://travis-ci.org/wallyqs/org-ruby/builds
  rspec -Ilib spec
  rm -rf spec
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.org
%{_bindir}/org-ruby
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.org

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.9.12-2
- 为 Magic 3.0 重建

* Fri Jan 02 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.12-1
- Update to org-mode 0.9.12 (RHBZ #1176963)
- rm superfluous "-p" flags to cp during %%install
- End -doc subpackage %%description with a period "."

* Thu Dec 18 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.10-1
- Update to org-mode 0.9.10 (RHBZ #1172647)

* Thu Sep 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.9-1
- Update to org-mode 0.9.9 (RHBZ #1129086)

* Thu Jul 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.7-1
- Update to org-mode 0.9.7 (RHBZ #1111884)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.6-1
- Update to org-mode 0.9.6 (RHBZ #1090021)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Tests are actually passing now, so don't throw away the exit code in %%check.

* Wed Apr 02 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.3-1
- Update to org-mode 0.9.3 (RHBZ #1080900)
- New upstream project location on GitHub

* Wed Feb 19 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.1-1
- Update to org-mode 0.9.1

* Mon Feb 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.0-1
- Update to org-mode 0.9.0
- Remove %%{gem_instdir}/bin/org-ruby from -doc sub-package

* Wed Feb 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.3-1
- Update to org-mode 0.8.3
- Adjust tests tarball generation script to tidy up after running

* Mon Dec 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.2-2
- Remove macro-in-comment for rpmlint

* Mon Dec 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.2-1
- Initial package
