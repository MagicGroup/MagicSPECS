# Generated from taskjuggler-3.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name taskjuggler

Summary: A Project Management Software
Name: rubygem-%{gem_name}
Version: 3.5.0
Release: 3%{?dist}
Group: Development/Languages
License: GPLv2
URL: http://www.taskjuggler.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(mail) >= 2.4.3
BuildRequires: rubygem-minitest
BuildRequires: rubygem-rspec
BuildRequires: rubygem(term-ansicolor) >= 1.0.7
BuildArch: noarch

%description
TaskJuggler is a modern and powerful, Free and Open Source Software project
management tool. Its new approach to project planing and tracking is more
flexible and superior to the commonly used Gantt chart editing tools.
TaskJuggler is project management software for serious project managers. It
covers the complete spectrum of project management tasks from the first idea
to the completion of the project. It assists you during project scoping,
resource assignment, cost and revenue planing, risk and communication
management.


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

%build

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# gem install installs into a directory.  We set that to be a local
# directory so that we can move it into the buildroot in install
%gem_install

%check
pushd .%{gem_instdir}
# The test cases does not work reliably.
mv ./test/test_BatchProcessor.rb{,.disable}

# Run the tests using minitest 5.
LANG=en_US.utf8 ruby -Ilib -rminitest/autorun - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end

  module Minitest::Assertions
    alias :assert_raise :assert_raises
  end

  Test = Minitest

  Dir.glob "./test/test_*.rb", &method(:require)
EOF

rspec -Ilib spec
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa ./%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa ./%{_bindir}/* \
        %{buildroot}%{_bindir}/

# Remove shebangs.
find %{buildroot}%{gem_instdir}/{lib,test,spec} -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/env ruby/d'

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gemtest
%{_bindir}/tj3
%{_bindir}/tj3client
%{_bindir}/tj3d
%{_bindir}/tj3man
%{_bindir}/tj3ss_receiver
%{_bindir}/tj3ss_sender
%{_bindir}/tj3ts_receiver
%{_bindir}/tj3ts_sender
%{_bindir}/tj3ts_summary
%{_bindir}/tj3webd
%{gem_instdir}/bin
%doc %{gem_instdir}/COPYING
# TODO: Includes VIM syntax highlighter, might be worth of extracting into
# subpackage?
%{gem_instdir}/data
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/examples
%doc %{gem_instdir}/manual
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/tasks
%{gem_instdir}/test


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3.5.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.5.0-2
- 为 Magic 3.0 重建

* Tue Jul 29 2014 Vít Ondruch <vondruch@redhat.com> - 3.5.0-1
- Update to TaskJuggler 3.5.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Josef Stribny <jstribny@redhat.com> - 3.4.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Tomas Dabasinskas <tomas@redhat.com> - 3.4.0-1
- Updating to 3.4.0

* Thu Oct 25 2012 Tomas Dabasinskas <tomas@redhat.com> - 3.3.0-3
- Updating the spec based on Russell's <rharrison@fedoraproject.org>
  rubygem-taskjuggler-3.3.0-3.fc19.spec
- Disabled Export-Reports and Syntax tests. Tests pass when called 
  via shell, but fail when called during rpmbuild, spec tests pass 
  when spec/*.rb is specified
- Updated prep and build sections
- Added doc subpackage

* Tue Oct 16 2012 Tomas Dabasinskas <tomas@redhat.com> - 3.3.0-2
- Fixing issues raised during package review
  * Source
  * deprecated parts in the spec file
  
* Thu Sep 06 2012 Tomas Dabasinskas <tomas@redhat.com> - 3.3.0-1
- Initial packaging effort

