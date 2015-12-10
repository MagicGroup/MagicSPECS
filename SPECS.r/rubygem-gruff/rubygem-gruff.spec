# Generated from gruff-0.3.4.gem by gem2rpm -*- rpm-spec -*-
%define gem_name gruff
%define installroot %{buildroot}%{gem_instdir}

Summary:	Beautiful graphs for one or multiple datasets
Name:		rubygem-%{gem_name}
Version:	0.3.6
Release:	11%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://nubyonrails.com/pages/gruff
Source0:	http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires:	rubygem(hoe) >= 1.12.1
Requires:	ruby-RMagick
BuildRequires: rubygems-devel
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}

%description
Beautiful graphs for one or multiple datasets. Can be used on websites or in
documents.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
gem install --local --install-dir %{buildroot}%{gem_dir} \
            --force --rdoc %{SOURCE0}

chmod +x %{installroot}/test/test_dot.rb
chmod +x %{installroot}/test/test_spider.rb
chmod +x %{installroot}/test/test_pie.rb
chmod +x %{installroot}/test/test_photo.rb
chmod +x %{installroot}/test/test_base.rb
chmod +x %{installroot}/test/test_stacked_area.rb
chmod +x %{installroot}/test/test_stacked_bar.rb
chmod +x %{installroot}/test/test_net.rb
chmod +x %{installroot}/test/test_sidestacked_bar.rb
chmod +x %{installroot}/test/test_area.rb
chmod +x %{installroot}/test/test_bar.rb
chmod +x %{installroot}/test/test_line.rb
chmod +x %{installroot}/test/test_scene.rb

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gem_dir}/gems/%{gem_name}-%{version}/
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%{gem_cache}
%{gem_spec}


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.3.6-11
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.3.6-10
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.6-9
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.6-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 24 2009 Darryl Pierce <dpierce@redhat.com> - 0.3.6-1
- Release 0.3.6 of Gruff.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 17 2008 Darryl Pierce <dpierce@redhat.com> - 0.3.4-3
- Added a requirement for ruby-RMagick.

* Mon Nov 10 2008 Darryl Pierce <dpierce@redhat.com> - 0.3.4-2
- Fixed the license for package review.

* Mon Oct 20 2008 Darryl Pierce <dpierce@redhat.com> - 0.3.4-1
- Initial packaging for review.
