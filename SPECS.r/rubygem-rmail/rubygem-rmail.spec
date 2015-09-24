# Generated from rmail-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rmail

Summary: A MIME mail parsing and generation library
Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 11%{?dist}
Group: Development/Languages
License: BSD
URL: http://rubyforge.org/projects/rubymail
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
# Patch rmail to use ASCII-8BIT in regexps and tests
# https://github.com/matta/rubymail/pull/2
# https://github.com/matta/rubymail/pull/3
Patch0: rubygem-rmail-1.0.0-ruby-2.0-use-ascii-8bit.patch
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%description
RMail is a lightweight mail library containing various utility classes and
modules that allow ruby scripts to parse, modify, and generate MIME mail
messages.


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
            
# Remove shebang from files that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && sed -i -e '/^#!\//, 1d' $file
done

# Remove install file
rm -f %{buildroot}%{gem_instdir}/install.rb

%check
pushd .%{gem_instdir}
testrb2 -I. -Ilib test/test*
rm -rf _scratch_*
popd

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/version
%doc %{gem_instdir}/README
%doc %{gem_instdir}/NEWS
%doc %{gem_instdir}/THANKS
%doc %{gem_instdir}/NOTES
%doc %{gem_instdir}/TODO
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%{gem_docdir}
%{gem_instdir}/test
%{gem_instdir}/guide
%{gem_instdir}/Rakefile

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.0-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 2 2010 Shreyank Gupta <sgupta@redhat.com> - 1.0.0-3
- Removed Requires:ruby(rubygems) from -docs subpackage
- Moved NEWS, THANKS, NOTES and TODO to main package
- dir ownership of geminstdir by main package
- gemdir/doc not owned by docs subpackage

* Tue Jun 1 2010 Shreyank Gupta <sgupta@redhat.com> - 1.0.0-2
- Removed ruby_sitelib macro
- Requires ruby(abi) and BuildRequires ruby and rake
- Added Subpackage -doc
- Remove isntall.rb
- Keeping zero-length file data.17 for rake test
- rake test added

* Mon May 31 2010 Shreyank Gupta <sgupta@redhat.com> - 1.0.0-1
- Initial package
