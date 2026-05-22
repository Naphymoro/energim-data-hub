document.addEventListener('DOMContentLoaded',function(){
  var right=document.querySelector('.nav-right');
  if(right&&!document.querySelector('.alpha-version-badge')){
    var badge=document.createElement('div');
    badge.className='cbadge on alpha-version-badge';
    badge.textContent='Alpha 0.1';
    right.insertBefore(badge,right.firstChild);
  }
  var nav=document.querySelector('.nav-tabs');
  var main=document.querySelector('.main');
  if(!nav||!main||document.getElementById('alpha')) return;
  var tab=document.createElement('button');
  tab.className='nt';
  tab.setAttribute('data-tab','alpha');
  tab.textContent='Alpha';
  nav.appendChild(tab);
  var panel=document.createElement('section');
  panel.className='tabpanel';
  panel.id='alpha';
  var title=document.createElement('div');
  title.className='ph';
  title.textContent='ENERGIM Alpha v0.1 - Rwanda-only modelling readiness layer';
  panel.appendChild(title);
  var notice=document.createElement('div');
  notice.className='alpha-ribbon';
  notice.textContent='Alpha release: outputs require expert validation before use in official LEAP, NEMO, or NDC reporting.';
  panel.appendChild(notice);
  var grid=document.createElement('div');
  grid.className='alpha-grid';
  [['2015','Baseline anchor'],['2015-2024','Historical calibration'],['2025-2035','NDC 3.0 planning']].forEach(function(x){var c=document.createElement('div');c.className='alpha-card';var b=document.createElement('div');b.className='big';b.textContent=x[0];var h=document.createElement('h3');h.textContent=x[1];var p=document.createElement('p');p.textContent='Rwanda-only scope with LEAP and NEMO interoperability scaffolding.';c.appendChild(b);c.appendChild(h);c.appendChild(p);grid.appendChild(c);});
  panel.appendChild(grid);
  main.appendChild(panel);
  tab.addEventListener('click',function(){document.querySelectorAll('.nt').forEach(function(x){x.classList.remove('active')});document.querySelectorAll('.tabpanel').forEach(function(x){x.classList.remove('active')});tab.classList.add('active');panel.classList.add('active');});
});
