%global gem_name git-up 
%global git_bindir %{_libexecdir}/git-core

Name: rubygem-%{gem_name}
Version: 0.5.12
Release: 5%{?dist}
Summary: git command to fetch and rebase all branches

Group: Development/Languages
License: MIT
URL: http://github.com/aanand/%{gem_name}
Source1: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

# use system ruby instead of ruby from environment
Patch1: 0001-bin-use-system-ruby.patch

BuildArch: noarch
BuildRequires: rubygems-devel
%if %{fedora} >= 19
Requires: ruby(release)
%endif
Requires: rubygems
Requires: rubygem-colored >= 1.2, rubygem-grit
Requires: git
Provides: rubygem(%{gem_name}) = %{version}

%description

Regular 'git pull' has two problems:

* It merges upstream changes by default, when it's really more polite to
  rebase over them, unless your collaborators enjoy a commit graph that looks
  like bedhead.

* It only updates the branch you're currently on, which means git push will
  shout at you for being behind on branches you don't particularly care about
  right now.

Solve them once and for all.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
Requires: rubygems-doc
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
gem unpack %{SOURCE1}
%setup -q -D -T -n %{gem_name}-%{version}
%patch1 -p1
gem spec %{SOURCE1} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{git_bindir}/git-core
ln -s ../../..%{gem_instdir}/bin/git-up %{buildroot}%{git_bindir}/git-up

rm -f %{buildroot}%{gem_cache}


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%{gem_spec}
%{gem_instdir}/bin
%{gem_instdir}/man
%{git_bindir}/git-up


%files doc
%doc %{gem_docdir}


%changelog
* Thu Jul 23 2015 Till Maas <opensource@till.name> - 0.5.12-5
- Rebuilt for https://fedoraproject.org/wiki/Deprecate_FTBFS_packages

* Fri Sep 13 2013 Jan Vcelak <jvcelak@fedoraproject.org> 0.5.12-4
- add missing rubygems-doc dependency for doc subpackage

* Fri Sep 13 2013 Jan Vcelak <jvcelak@fedoraproject.org> 0.5.12-3
- add missing rubygem(git-up) Provides

* Thu Sep 12 2013 Jan Vcelak <jvcelak@fedoraproject.org> 0.5.12-2
- add comments to patches
- install (cp) with preserved attributes
- remove cached Gem from the package

* Wed Sep 11 2013 Jan Vcelak <jvcelak@fedoraproject.org> 0.5.12-1
- update to newer version

* Sun Mar 31 2013 Jan Vcelak <jvcelak@fedoraproject.org> 0.5.8-1
- initial package
