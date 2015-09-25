%global gem_name joiner

Name: rubygem-%{gem_name}
Version: 0.3.4
Release: 3%{?dist}
Summary: Builds ActiveRecord joins from association paths
Group: Development/Languages
License: MIT
URL: https://github.com/pat/joiner
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(activerecord) >= 4.1.0
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rails) >= 4.1.2
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rspec-rails)
BuildRequires: rubygem(sqlite3)
# combustion is yet in Fedora. Review request at
# https://bugzilla.redhat.com/1117022
#BuildRequires: rubygem(combustion)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Builds ActiveRecord outer joins from association paths and provides references
to table aliases.


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

for f in .gitignore Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Remove dependency on bundler.
sed -i "/bundle/Id" spec/spec_helper.rb

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  # rubygem-combustion is not yet in Fedora, so the test suite fails.
  # combustion review request at https://bugzilla.redhat.com/1117022
  rspec -Ilib spec || :
popd


%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.4-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Nov 20 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.4-1
- Update to joiner 0.3.4 (RHBZ #1166413)
- BR rails > 4.1.2 to match gemspec's version
- Drop upstreamed patch for loading ActiveRecord outside bundler
- Drop redundant "-p" argument to cp
- Update -doc subpackage description to match convention in Fedora

* Fri Oct 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.3-1
- Update to joiner 0.3.3 (RHBZ #1117025)
- Use %%license macro (RHBZ #1117025)

* Wed May 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.0-1
- Initial package
