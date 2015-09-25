%global gem_name gemcutter

Summary:        The gemcutter client gem
Name:           rubygem-%{gem_name}
Version:        0.3.0
Release:        13%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://gemcutter.org
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(release)
Requires:	ruby(rubygems)
Requires:       rubygem(json)
BuildRequires:	rubygems-devel
#BuildRequires:	rubygem(webmock)
BuildRequires:	rubygem(shoulda)
BuildRequires:	rubygem(activesupport)
BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(rr)
BuildRequires:  dos2unix
# For test
#BuildRequires:  rubygem(shoulda)

BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
The gemcutter client gem that interacts with the site http://gemcutter.org

%prep
%setup -q -T -c
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}

# bug 570254
grep -rl json_pure . | xargs sed -i -e 's|json_pure|json|'

mkdir -p %{buildroot}/%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}/%{gem_dir}/.

dos2unix %{buildroot}/%{gem_instdir}/MIT-LICENSE

%check
pushd ./%{gem_instdir}
#TODO: test when webmock and rr get to rawhide
#rake test || :
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{gem_docdir}
%dir %{gem_instdir}/
%doc %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/Rakefile
%{gem_libdir}
%{gem_instdir}/test
%attr(0644,root,root) %{gem_cache}
%{gem_spec}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.0-13
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.0-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.0-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.0-3
- Require rubygem(json), replace json_pure with json
  (bug 570254)

* Sat Jan  9 2010 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3.0-2
- Fix end-of-line encoding in MIT-LICENSE file
- First package
