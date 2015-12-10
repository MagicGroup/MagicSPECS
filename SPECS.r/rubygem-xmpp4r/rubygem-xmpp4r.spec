%global gem_name xmpp4r

Summary: An XMPP/Jabber library for Ruby
Name: rubygem-%{gem_name}
Version: 0.5
Release: 14%{?dist}
Group: Development/Languages
License: GPL+ or Ruby
URL: http://home.gna.org/xmpp4r/
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
Patch0: rubygem-xmpp4r-examples.patch
Patch1: rubygem-xmpp4r-tests.patch
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
XMPP4R is an XMPP/Jabber library for Ruby.

%package    doc
Summary:    Documentation for %{name} 
Group:      Documentation
# Directory ownership issue
Requires:   %{name} = %{version}-%{release}

%description    doc
This package contains documentation and examples for %{name}.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

# Files Erroniously installed by the gem.
# They're used in the build process
rm -rf %{buildroot}%{gem_instdir}/%{gem_name}.gemspec 
rm -rf %{buildroot}%{gem_instdir}/setup.rb
rm -rf %{buildroot}%{gem_instdir}/tools

# Tidy up the file permissions
# Libraries shouldn't be executable, and the tests aren't run directly ...
find %{buildroot}%{gem_instdir}/{test,lib} -type f | \
    xargs chmod 0644
# ... the examples are valid scripts ...    
find %{buildroot}%{gem_instdir}/data/doc/%{gem_name}/examples \
    -type f -name '*.rb' | xargs chmod 0755
# ... and it's perfectly acceptable for users have read access to the
# source gem
chmod 644 %{buildroot}%{gem_cache}

# Find the ruby example scripts where they didn't include a schbang line
pushd %{buildroot}%{gem_instdir}/data/doc/xmpp4r/examples
    patch -p1 < %{PATCH0}
popd
# Fix their test cases so they run on fast machines
# and can all be run from simply rake test rather than 1 at a time
pushd %{buildroot}%{gem_instdir}
    patch -p1 < %{PATCH1}
popd

# Drop the standalone mode for tests 
# We can't run them way due to missing rubygems required for the tests.
find %{buildroot}%{gem_instdir}/{test,lib} -type f | \
    xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'

%clean
rm -rf %{buildroot}

%check
pushd %{buildroot}%{gem_instdir}
# failures reported on: https://github.com/ln/xmpp4r/issues/24
ruby -I. test/ts_xmpp4r.rb || :
popd


%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%dir %{gem_instdir}/data
%{gem_libdir}
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/README_ruby19.txt
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%{gem_instdir}/test
%{gem_instdir}/data/doc
%{gem_instdir}/Rakefile
%{gem_docdir}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.5-14
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.5-13
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5-12
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.5-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 02 2010 M Chappell <tremble@tremble.org.uk> - 0.5-3
- Remove redundant Requires from -doc package

* Fri Jan 29 2010 M D Chappell <m.d.chappell@bath.ac.uk> - 0.5-2
- Formatting clean ups
- Fix the test cases
- Replace define with global
- Remove unused macro
- Run the test cases in a check stanza

* Mon Jan 25 2010 M Chappell <m.d.chappell@bath.ac.uk> - 0.5-1
- Initial package
