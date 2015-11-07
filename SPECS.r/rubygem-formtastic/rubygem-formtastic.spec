# Generated from formtastic-1.2.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name formtastic

Name: rubygem-%{gem_name}
Version: 3.1.3
Release: 3%{?dist}
Summary: A Rails form builder plugin with semantically rich and accessible markup
Group: Development/Languages
License: MIT
URL: http://github.com/justinfrench/formtastic
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

%description
Formtastic is a Rails FormBuilder DSL (with some other goodies) to make it far
easier to create beautiful, semantically rich, syntactically awesome, readily
stylable and wonderfully accessible HTML forms in your Rails applications.

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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
# Get rid of Bundler.
sed -i '/bundler\/setup/ s/^/#/' spec/spec_helper.rb

# The test suite heavily depends on rspec_tag_matchers, which are not in
# Fedora yet :/
# rspec spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/app
%{gem_libdir}
# This is not the original file, no reason to keep it.
%exclude %{gem_instdir}/formtastic.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CHANGELOG
%{gem_instdir}/DEPRECATIONS
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.textile
%doc %{gem_instdir}/RELEASE_PROCESS
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles
%{gem_instdir}/sample
%{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 3.1.3-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.1.3-2
- 为 Magic 3.0 重建

* Thu Jun 25 2015 Vít Ondruch <vondruch@redhat.com> - 3.1.3-1
- Update to Formtastic 3.1.3.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Josef Stribny <jstribny@redhat.com> - 1.2.3-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.2.3-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 20 2011 Daiki Ueno <dueno@redhat.com> - 1.2.3-4
- Remove duplicate Requires for ruby.
- Remove docs from the main package.
- Drop cleaning %%{buildroot}.
- Rearrange files list of the main package.

* Wed Apr 20 2011 Daiki Ueno <dueno@redhat.com> - 1.2.3-3
- Improvide summary and description.
- Subpackage doc files.
- Remove versioned Requires so that yum should always pull latest
  dependencies.

* Wed Apr 20 2011 Daiki Ueno <dueno@redhat.com> - 1.2.3-2
- Fix License field.
- Remove unnecessary version requirements from Requires and BR.

* Tue Apr 19 2011 Daiki Ueno <dueno@redhat.com> - 1.2.3-1
- Initial package
