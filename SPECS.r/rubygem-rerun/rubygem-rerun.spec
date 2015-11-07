%global gem_name rerun


Summary: Restarts your app when a file changes
Name: rubygem-%{gem_name}
Version: 0.10.0
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/alexch/rerun/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/alexch/rerun.git && cd rerun
# git checkout v0.10.0 && tar czvf rerun-0.10.0-tests.tgz spec/ inc.rb
Source1: %{gem_name}-%{version}-tests.tgz
# Support rubygem-listen 3.0
Patch0: rubygem-rerun-listen3.patch
# Update listen dependency in gemspec
Patch1: rubygem-rerun-listen3-gemspec.patch
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(listen)
BuildRequires: rubygem(rb-inotify)
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
Launches an app, and restarts it whenever the filesystem changes

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

pushd .%{gem_dir}
%patch1 -p1
popd


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

# We don't have wrong in Fedora yet.
sed -i '/wrong/,/Wrong/ s/^/#/' spec/spec_helper.rb
mv spec/options_spec.rb{,.disabled}

# Fix RSpec 3.x compatibility.
sed -i 's|runner.clear?.should be_true|expect(runner.clear?).to be true|' spec/runner_spec.rb

# This fails in upstream due to change in Listen 2.7.5:
# https://github.com/guard/listen/commit/e3b7e23f9588599fb0daed4e030bab09c1c1507
# Return back to original values from:
# https://github.com/alexch/rerun/commit/04c94bd1ebab61f38f888d6909642cc28477e130
sed -i 's/Listen::Silencer::DEFAULT_IGNORED_DIRECTORIES/%w(.bundle .git .hg .rbx .svn bundle log tmp)/' spec/watcher_spec.rb

rspec spec
popd

%files
%{_bindir}/rerun
%{gem_instdir}/icons
%{gem_libdir}
%{gem_instdir}/bin
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/rerun.gemspec
%license %{gem_instdir}/LICENSE
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.10.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.10.0-4
- 为 Magic 3.0 重建

* Wed Aug 19 2015 Josef Stribny <jstribny@redhat.com> - 0.10.0-3
- Fix: work with rubygem-listen 3.x

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 0.10.0-1
- Update to rerun 0.10.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 0.6.2-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 0.6.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Vít Ondruch <vondruch@redhat.com> - 0.6.2-1
- Updated to rerun 0.6.2.
- Make tests working.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.5.2-3
- Fixed inconsistent changelog entry

* Wed May 05 2010 Michal Fojtik <mfojtik@redhat.com> - 0.5.2-2
- Fixed wrong patch in test
- Added --no-ri into gem install

* Fri Apr 30 2010 Michal Fojtik <mfojtik@redhat.com> - 0.5.2-1
- Initial package
