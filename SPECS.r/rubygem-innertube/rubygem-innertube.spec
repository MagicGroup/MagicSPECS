%global gem_name innertube

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 4%{?dist}
Summary: A thread-safe resource pool
Group: Development/Languages
License: ASL 2.0
URL: http://github.com/basho/innertube
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Upstream does not yet include the full text of the ASL 2.0 license in any
# released version of the gem. In the next release, we can drop this external
# file. See https://github.com/basho/innertube/pull/5
# This Source1 file is available at
# https://raw.github.com/basho/innertube/master/LICENSE
Source1: innertube-LICENSE
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Innertube is a thread-safe, re-entrant resource pool, extracted from the Riak
Ruby Client, where it was used to pool connections to Riak.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Remove developer-only file
# https://github.com/basho/innertube/pull/6
rm .gitignore
sed -i 's|".gitignore",\?||g' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary developer-only file
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Until upstream ships the full text of the ASL 2.0 in a released gem, we will
# ship the version from Git master.
install -p -m 0644 %{SOURCE1} %{buildroot}%{gem_instdir}/LICENSE

%check
pushd .%{gem_instdir}
  rspec spec
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/spec


%changelog
* Sat Jul 12 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-4
- Remove all occurrences of .gitignore in gemspec (RHBZ #1107143)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 30 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-2
- Rename Source1 (LICENSE) to have an innertube- prefix.
  Suggested during package review request (RHBZ #1024152)

* Sat Oct 12 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-1
- Initial package
