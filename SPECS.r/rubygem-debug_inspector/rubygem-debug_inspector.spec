# Generated from debug_inspector-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name debug_inspector

Name: rubygem-%{gem_name}
Version: 0.0.2
Release: 3%{?dist}
Summary: A Ruby wrapper for the MRI 2.0 debug_inspector API
Group: Development/Languages
License: MIT
URL: https://github.com/banister/debug_inspector
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel

%description
A Ruby wrapper for the MRI 2.0 debug_inspector API.


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

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

chmod -x %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/Rakefile

%check
pushd .%{gem_instdir}
# No upstream test suite available :/ but we can do some smoke test :)
ruby -Ilib:$(dirs +1)%{gem_extdir_mri} - << \EOF | grep '#<Class:RubyVM::DebugInspector>'
  require 'debug_inspector'

  # Open debug context
  # Passed `dc' is only active in a block
  RubyVM::DebugInspector.open { |dc|
    # backtrace locations (returns an array of Thread::Backtrace::Location objects)
    locs = dc.backtrace_locations

    # class of i-th caller frame
    p dc.frame_class(0)
  }
EOF
popd


%files
%doc %{gem_instdir}/README.md
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/debug_inspector.gemspec


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Vít Ondruch <vondruch@redhat.com> - 0.0.2-2
- Update to recent guidelines + review fixes.

* Mon May 06 2013 Anuj More - 0.0.2-1
- Initial package
